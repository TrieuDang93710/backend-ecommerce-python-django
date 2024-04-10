from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from user.models import UserAccount


# Tạo một custom serializer kế thứa từ UserCreateSerializer
class UserAccountSerializer(UserCreateSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'phone', 'address')


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')
