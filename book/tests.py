from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class BookManagementTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create(name="user1", email="a@a.com", password="password123")
        self.user2 = User.objects.create(name="user2", email="a2@a.com", password="password123")

        # Create a book published by user1
        self.book = Book.objects.create(
            title='Test Book',
            author=self.user1,
            description='A test book.',
            cover=SimpleUploadedFile("cover.jpg", b"file_content", content_type="image/jpeg")
        )

        # URLs
        self.publish_book_url = reverse('book-create-list')
        self.list_books_url = reverse('book-create-list')
        self.retrieve_book_url = reverse('book-detail', kwargs={'id': self.book.id})
        self.update_book_url = reverse('book-detail', kwargs={'id': self.book.id})
        self.delete_book_url = reverse('book-detail', kwargs={'id': self.book.id})

    def test_publish_book_authenticated(self):
        # Test publishing a book by an authenticated user
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Book',
            'description': 'A new book.',
            'cover': SimpleUploadedFile(
                    name="sample.jpeg",
                    content=open("book/sample.jpeg", "rb").read(),
                    content_type="image/jpeg"
                ),
            'slug': 'new-book'
        }
        response = self.client.post(self.publish_book_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Ensure the book was created

    def test_publish_book_unauthenticated(self):
        # Test publishing a book by an unauthenticated user
        data = {
            'title': 'New Book',
            'description': 'A new book.',
            'cover': SimpleUploadedFile("new_cover.jpg", b"file_content", content_type="image/jpeg")
        }
        response = self.client.post(self.publish_book_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 1)  # Ensure no book was created

    def test_list_all_books(self):
        # Test listing all books
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'] , 1 )  # Ensure the book is in the list

    def test_retrieve_specific_book(self):
        # Test retrieving a specific book by its ID
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.retrieve_book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')  # Ensure the correct book is retrieved

    def test_update_book_by_owner(self):
        # Test updating a book by the owner
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Updated Book Title',
            'description': 'Updated description.'
        }
        response = self.client.patch(self.update_book_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')  # Ensure the book was updated

    def test_update_book_by_non_owner(self):
        # Test updating a book by a non-owner
        self.client.force_authenticate(user=self.user2)
        data = {
            'title': 'Unauthorized Update',
            'description': 'Unauthorized description.'
        }
        response = self.client.patch(self.update_book_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Test Book')  # Ensure the book was not updated

    def test_delete_book_by_owner(self):
        # Test deleting a book by the owner
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())  # Ensure the book was deleted

    def test_delete_book_by_non_owner(self):
        # Test deleting a book by a non-owner
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.delete_book_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())  # Ensure the book was not deleted