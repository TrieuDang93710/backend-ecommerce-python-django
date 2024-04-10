from django.urls import path
from upload import views
urlpatterns = [
    path("upload-images/", views.PhotoAPIView.as_view()),
]
