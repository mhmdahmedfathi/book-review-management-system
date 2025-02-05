from django.db import models

class Review(models.Model):
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"