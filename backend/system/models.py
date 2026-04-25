from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', '寺廟管理員'
    VOLUNTEER = 'Volunteer', '志工'

class AccountStatusChoices(models.TextChoices):
    ACTIVE = 'Active', '啟用'
    INACTIVE = 'Inactive', '停用'
    SUSPENDED = 'Suspended', '停權'

class UserAccountManager(BaseUserManager):
    def create_user(self, account, email, password=None, **extra_fields):
        if not account:
            raise ValueError('Account must be set')
        email = self.normalize_email(email)
        user = self.model(account=account, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account, email, password=None, **extra_fields):
        extra_fields.setdefault('role', RoleChoices.ADMIN)
        extra_fields.setdefault('Account_Status', AccountStatusChoices.ACTIVE)
        return self.create_user(account, email, password, **extra_fields)

class User_Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.VOLUNTEER) # 角色(寺廟管理員/志工)
    email = models.CharField(max_length=255)
    account = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, db_column='password_hash', unique=True)
    Account_Status = models.CharField(max_length=50, choices=AccountStatusChoices.choices, default=AccountStatusChoices.ACTIVE)
    Account_Creation_Time = models.DateTimeField(auto_now_add=True)
    Account_Update_Time = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'User_Account'

    def __str__(self):
        return self.account
