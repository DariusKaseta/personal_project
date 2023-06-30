from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import AboutMeForm, PersonalInformationForm
from create_scrape_send.models import AboutMe, PersonalInformation
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

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
        print(about_me_form.errors)
        print(personal_info_form.errors)
    context = {
        'about_me_form': about_me_form,
        'personal_info_form': personal_info_form,
        }
    return render(request, "user_profile/create.html", context) 
