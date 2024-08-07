from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return f"Avatar {self.id}"

    class Meta:
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'


class UserManager(BaseUserManager):
    def create_user(self, username, fullname, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        username = username.lower()
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
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message='Username can only contain letters, numbers, and underscores.'
    )

    username = models.CharField(max_length=20, unique=True, validators=[username_validator])
    fullname = models.CharField(max_length=30)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        super(User, self).save(*args, **kwargs)

    def update_profile(self, fullname=None, avatar=None):
        if fullname:
            self.fullname = fullname
        if avatar:
            self.avatar = avatar
        try:
            self.save()
        except ValidationError as e:
            raise ValidationError(f'Error updating profile: {e}')


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
