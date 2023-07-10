from django.urls import path, include
from . import views
from .views import ScrapedEmailsView


# APP urls

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", include("user_profile.urls")),
    path("scrape/search/", views.ScrapedEmailsView.as_view(), name="search"),
    
]
