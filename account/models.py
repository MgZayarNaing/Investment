import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from customer.models import *

class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    MANAGER = 'manager'
    INVESTER = 'invester'

    ROLES_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (INVESTER,'Invester'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.BigIntegerField(default=None,null=True,blank=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default=INVESTER)
    phone = PhoneNumberField(null=True,blank=True)

    profile = models.ImageField(default=None,null=True,blank=True)
    address = models.TextField(default=None,null=True,blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']