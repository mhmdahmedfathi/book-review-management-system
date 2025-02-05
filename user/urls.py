from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user-create'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
]