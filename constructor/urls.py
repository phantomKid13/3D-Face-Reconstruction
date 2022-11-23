from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload", views.upload, name="upload"),
    path("cam_upload", views.cam_upload, name="cam_upload"),
    path("cam", views.cam, name="cam"),
    path("lab", views.lab, name="lab"),
    path("viewer", views.viewer, name="viewer"),
    path("generate", views.generate, name="generate")
]