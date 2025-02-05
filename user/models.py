from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    join_date = models.DateTimeField(auto_now_add=True)

    # This is required for the custom user model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    @property
    def is_staff(self):
        return self.is_admin