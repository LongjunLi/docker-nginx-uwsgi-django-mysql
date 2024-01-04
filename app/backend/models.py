from django.db import models

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username cannot be empty!")
        if not password:
            raise ValueError("Password cannot be empty!")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, blank=False, null=False)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "t_user_info"


class UserInfoDelete(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=False, null=False)
    user_info_id = models.BigIntegerField(blank=False, null=False)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "t_user_info_delete"


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "t_item"


class ItemDelete(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.BigIntegerField(blank=False, null=False)
    operate_user_id = models.BigIntegerField(blank=False, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "t_item_delete"
