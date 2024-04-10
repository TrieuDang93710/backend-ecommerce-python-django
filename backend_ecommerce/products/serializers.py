from . import models
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        # sử dụng __all__ để serializer tất cả các field được khai báo trong model
        fields = '__all__'


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductComment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # Sử dụng serializer để tạo ra list record con trước,
    # sau đó add vào product serializer dưới cái tên images
    # *Lưu ý: tên này cần phải trùng với option related_name đã khai báo trong model
    # many=True để convert các field thành một array, nếu không serializer sẽ chỉ trả về 1 single object
    # read_only=True đảm bảo rằng field này không thể được cập nhật thông qua API
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        # Khai báo từng field cụ thể, thêm custom field images và comments
        fields = (
            'id',
            'name',
            'unit',
            'price',
            'discount',
            'amount',
            'is_public',
            'thumbnail',
            'images',
            'comments',
            'category_id',
            'created_at',
            'updated_at',
            'deleted_at'
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = (
            'id',
            'name',
            'slug',
            'icon_url',
            'products',
            'created_at',
            'updated_at',
            'deleted_at'
        )
