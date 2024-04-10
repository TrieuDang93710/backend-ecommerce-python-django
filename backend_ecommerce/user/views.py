from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from backend_ecommerce.helpers import custom_response
from user.serializers import UserAccountSerializer, UserAccountUpdateSerializer
from rest_framework import views
# Create your views here.


class UserAccountUpdateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserAccountSerializer(request.user)
        return custom_response('Get user successfully!', 'Success', serializer.data, 200)

    def put(self, request, *args, **kwargs):
        serializer = UserAccountUpdateSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Update user successfully!', 'Success', serializer.data, 200)
        return custom_response('Update user failed!', 'Error', serializer.errors, 400)
