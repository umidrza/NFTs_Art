from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return f"Avatar {self.id}"


class UserManager(BaseUserManager):
    def create_user(self, username, fullname, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, fullname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    fullname = models.CharField(max_length=30)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.username

    def update_profile(self, fullname=None, avatar=None):
        if fullname:
            self.fullname = fullname
        if avatar:
            self.avatar = avatar
        self.save()