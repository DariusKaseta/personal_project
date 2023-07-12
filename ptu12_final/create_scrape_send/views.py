from django.shortcuts import render
from .models import AboutMe, PersonalInformation, Email
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView
from django.db.models import Q
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.http import HttpResponse


@login_required
def index(request):
    personal_info_data = PersonalInformation.objects.filter(user=request.user).first()
    about_me_data = AboutMe.objects.filter(user=request.user).first()
    context = {
        "about_me_data": about_me_data,
        "personal_info_data": personal_info_data,
    }
    return render(request, "create_scrape_send/index.html", context=context)


class ScrapedEmailsView(ListView):
    model = Email
    template_name = "user_profile/scraped_emails.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
                Q(address__icontains=query)
            )
        return queryset


