from django.urls import path
from . import views


# APP urls

urlpatterns = [
    path("", views.index, name="index")
]
