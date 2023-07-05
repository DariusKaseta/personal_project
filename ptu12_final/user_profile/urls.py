from django.urls import path
from . import views
from .views import search_bar, SendEmailView, success_message_view, error_message_view

# user_profile URLs


urlpatterns = [
    path("create/", views.create, name="create"),
    path("scrape/", views.scrape, name="scrape"),
    # path("scrape/search/", views.search_bar, name="search_bar"), # neveikia search bar dar
    path('send/email/', SendEmailView.as_view(), name='send_emails'),
    path("success/", views.success_message_view, name="success_message"),
    path("error/", views.error_message_view, name="error_message"),
]
