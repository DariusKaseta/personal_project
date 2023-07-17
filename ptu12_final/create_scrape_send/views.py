from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import AboutMe, PersonalInformation, Email
from operator import or_
from functools import reduce
from django.views import generic


@login_required
def index(request):
    personal_info_data = PersonalInformation.objects.filter(user=request.user).first()
    about_me_data = AboutMe.objects.filter(user=request.user).first()
    context = {
        "about_me_data": about_me_data,
        "personal_info_data": personal_info_data,
    }
    return render(request, "create_scrape_send/index.html", context=context)


class ScrapedEmailsSearchView(ListView):
    model = Email
    template_name = "user_profile/scraped_emails.html"
    search_fields = ["address"]
        
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get("query")
        if search_term:
            search_words = search_term.split()
            if search_words:
                q_objects = [Q(**{field + '__icontains': word}) for field in self.search_fields for word in search_words]
                queryset = queryset.filter(reduce(Q.__or__, q_objects))
            else:
                queryset = queryset.none()
        else:
            queryset = queryset.none()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get("query", "")
        context['search_term'] = search_term
        context['result_count'] = self.get_queryset().count()
        return context

