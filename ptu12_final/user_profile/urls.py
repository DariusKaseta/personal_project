from django.urls import path
from . import views
from .views import SendEmailView , success_message_view, error_message_view

# user_profile URLs


urlpatterns = [
    path("create/", views.create, name="create"),
    path("scrape/", views.scrape, name="scrape"),
    path('send/email/', views.SendEmailView.as_view(), name='send_emails'),
    path("success/", views.success_message_view, name="success_message"),
    path("error/", views.error_message_view, name="error_message"),
]
