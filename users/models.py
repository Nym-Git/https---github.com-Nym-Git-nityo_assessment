from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid


class UserManager(BaseUserManager):
  def create_user(self, user_name, password, is_active):
    user = self.model(user_name=user_name, is_active=is_active)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, user_name, password, is_active):
    user = self.create_user(user_name=user_name, password=password, is_active=is_active)
    user.is_active = True
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user
  
  def create_admin(self, email, password, is_active):
    user = self.create_user(email=email, password=password, is_active=is_active)
    user.is_active = is_active
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = False
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
  user_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'user_name'
  REQUIRED_FIELDS = ['password','is_active']

  class Meta:
    app_label = 'users'

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_prems(self, add_lable):
    return True