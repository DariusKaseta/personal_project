from django.urls import path
from . import views

# user_profile URLs


urlpatterns = [
    path("create/", views.create, name="create")
]
