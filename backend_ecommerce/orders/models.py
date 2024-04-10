from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from products.models import Product
# Create your models here.


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    receiver_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=15)
    receiver_address = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    description = models.CharField(max_length=512)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details',
                                 null=False)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


# Tự động trigger cập nhật giá tổng của đơn hàng khi price và discount của order detail thay đổi
@receiver([post_save, post_delete], sender=OrderDetail)
def update_order_total(sender, instance, **kwargs):
    order = instance.order_id
    total = sum((detail.price - (detail.price * detail.discount / 100)) * detail.amount
                for detail in order.order_details.all())
    order.total = total
    order.save()
