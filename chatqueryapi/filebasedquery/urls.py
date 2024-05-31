from django.urls import path
from .views import UploadAPIView, ChatAPIView

urlpatterns = [
    path("upload-file/", UploadAPIView.as_view(), name = "upload-file"),
    path("chat/", ChatAPIView.as_view(), name = "chat-api"),
]
