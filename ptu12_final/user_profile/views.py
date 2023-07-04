from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_protect
from .forms import AboutMeForm, PersonalInformationForm, EmailForm
from create_scrape_send.models import AboutMe, PersonalInformation, SendScraped, Email
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import generic
from random import sample
from typing import Any
import math
import requests
import re 
from selenium import webdriver 
from django.utils.translation import gettext_lazy as _

# Create your views here.
User = get_user_model()

@csrf_protect
@login_required
def create(request):
    if request.method =="POST":
        print(f"User: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated}")

        about_me_form = AboutMeForm(request.POST)
        personal_info_form = PersonalInformationForm(request.POST, request.FILES)

        if about_me_form.is_valid() and personal_info_form.is_valid():
            personal_info = personal_info_form.save(commit=False)
            personal_info.user = request.user
            personal_info.picture = request.FILES.get('picture')
            personal_info.save()
            
            about_me = about_me_form.save(commit=False)
            about_me.user = request.user
            about_me.personal_information = personal_info
            about_me.save()
            return redirect("index")
    else:
        about_me_form = AboutMeForm()
        personal_info_form = PersonalInformationForm()
    context = {
        'about_me_form': about_me_form,
        'personal_info_form': personal_info_form,
        }
    return render(request, "user_profile/create.html", context) 


@csrf_protect
@login_required
def scrape(request):
    safari_driver = '/Users/ciliukas/CodeAcademy/drivers/chromedriver'
    driver = webdriver.Safari(safari_driver)
    driver.get('https://www.randomlists.com/email-addresses?qty=1000')
    page_source = driver.page_source
    EMAIL_REGEX = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
    list_of_emails = []
    
    for re_match in re.finditer(EMAIL_REGEX, page_source):
        list_of_emails.append(re_match.group())
    driver.close()
        
    random_emails = sample(list_of_emails, k=min(len(list_of_emails), 1001))
    random_emails = random_emails[:1001]
    existing_emails_count = Email.objects.filter(user=request.user).count()
    emails_to_create = 1001 - existing_emails_count

    for email_address in random_emails[:emails_to_create]:
        Email.objects.get_or_create(address=email_address, user=request.user)
    email_count = Email.objects.filter(user=request.user).count()
    
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            send_instance = SendScraped(user=request.user)
            send_instance.save()
            send_instance.emails.set(form.cleaned_data['emails'])
    else:
        form = EmailForm()
    queryset = Email.objects.filter(user=request.user)
    paginator = Paginator(queryset, 50) 
    page_number = request.GET.get("page")
    scrape_list = paginator.get_page(page_number)
    page_range = range(1, paginator.num_pages + 1)
    return render(
        request, 
        "user_profile/scraped_emails.html", 
        {   "form": form,
            "email_count": email_count,
            "scrape_list": scrape_list,
            "page_range": page_range,
        }
    )