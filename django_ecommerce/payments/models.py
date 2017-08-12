from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    # password field defined in base class
    last_4_digits = models.CharField(max_length=4, blank=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    @classmethod
    def get_by_id(cls, uid: int):
        return User.objects.get(pk=uid)

    @classmethod
    def create(cls, name: str, email: str, password: str, last_4_digits: str,
               stripe_id: str):
        new_user = cls(name=name,
                       email=email,
                       last_4_digits=last_4_digits,
                       stripe_id=stripe_id)
        new_user.set_password(password)

        new_user.save()
        return new_user

    def __str__(self):
        return self.email


class UnpaidUser(models.Model):
    email = models.CharField(max_length=255, unique=True)
    last_notification = models.DateTimeField(auto_now=True)
