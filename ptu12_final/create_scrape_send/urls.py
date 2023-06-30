from django.urls import path, include
from . import views


# APP urls

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", include("user_profile.urls")),
    
]
