from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.IntegerField(default=None, blank=True, null=True)
    # email = models.EmailField(max_length=255, default=None, blank=True, null=True)

    def is_valid(self):
        pass


# class UserInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#
#     def __str__(self):
#         return self.user.username



