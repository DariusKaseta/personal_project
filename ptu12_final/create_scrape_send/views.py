from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import AboutMe, PersonalInformation
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

@login_required
def index(request):
    personal_info_data = PersonalInformation.objects.filter(user=request.user).first()
    about_me_data = AboutMe.objects.filter(user=request.user).first()
    context = {
        "about_me_data": about_me_data,
        "personal_info_data": personal_info_data,
    }
    return render(request, "create_scrape_send/index.html", context=context)
