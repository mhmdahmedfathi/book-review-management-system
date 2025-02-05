from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:id>/', views.ReviewDetail.as_view(), name='review-retrieve-update-destroy'),
    path('book/<int:id>/', views.BookReviewList.as_view(), name='book-review-list'),
]