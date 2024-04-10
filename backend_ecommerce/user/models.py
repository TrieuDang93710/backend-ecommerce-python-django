from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Kế thừa AbstractUser để có thể thêm các trường vào User model
# Không thể dùng từ khóa User nên sẽ thay thế bằng UserAccount


class UserAccount(AbstractUser):
    # Định nghĩa các trường cần thêm vào User model
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        # Định nghĩa ENUM
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')]
    )
