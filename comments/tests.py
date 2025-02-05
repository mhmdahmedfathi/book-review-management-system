from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from book.models import Book
from user.models import User
from .models import Review

class ReviewDetailTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create(name="user1", email="a@a.com", password="password123")
        self.user2 = User.objects.create(name="user2", email="a2@a.com", password="password123")

        # Create a book published by user1
        self.book = Book.objects.create(title='Test Book', author=self.user1, description='A test book.', slug='test-book')

        # Create a review by user2 on the book
        self.review = Review.objects.create(
            book=self.book,
            user=self.user2,
            comment='Great book!',
        )

        # URL for the review detail view
        self.url = reverse('review-retrieve-update-destroy', kwargs={'id': self.review.id})

    def test_retrieve_review(self):
        # Test retrieving a review
        # authenticate user1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Great book!')

    def test_update_review_by_owner(self):
        # Test updating a review by the owner
        self.client.force_authenticate(user=self.user2)
        data = {'comment': 'Updated comment'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'Updated comment')

    def test_update_review_by_non_owner(self):
        # Test updating a review by a non-owner
        self.client.force_authenticate(user=self.user1)
        data = {'comment': 'Unauthorized update'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, 'Great book!')  # Ensure the review was not updated

    def test_delete_review_by_owner(self):
        # Test deleting a review by the owner
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_by_non_owner(self):
        # Test deleting a review by a non-owner
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())  # Ensure the review was not deleted

    def test_update_review_user_field(self):
        # Test that the user field cannot be updated
        self.client.force_authenticate(user=self.user2)
        data = {'user': self.user1.id}  # Attempt to change the user
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.user.id, self.user2.id)  # Ensure the user field was not updated

    def test_update_review_book_field(self):
        # Test that the book field cannot be updated
        self.client.force_authenticate(user=self.user2)
        new_book = Book.objects.create(title='New Book', author=self.user1, description='Another test book.', slug='new-book')
        data = {'book': new_book.id}  # Attempt to change the book
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.book.id, self.book.id)  # Ensure the book field was not updated