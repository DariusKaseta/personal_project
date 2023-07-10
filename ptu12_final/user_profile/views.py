from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.views import View
from django.views import generic
from django.shortcuts import render, redirect
from .forms import AboutMeForm, PersonalInformationForm, EmailForm, SendForm
from create_scrape_send.models import SendScraped, Email
from django.utils.translation import gettext_lazy as _
from random import sample
from typing import Any
import re 
from selenium import webdriver 

# Create your views here.
User = get_user_model()

@csrf_protect
@login_required
def create(request):
    if request.method == "POST":
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


def scrape(request):
    # Tikrinimas ar jau useris turi email .db, kad kas kart nescrapintu
    if cache.get(f"send_emails_{request.user.id}"):
        email_count = Email.objects.filter(user=request.user).count()
    else:
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
        # Tikrinimas ar jau useris turi email .db, kad kas kart nescrapintu
        cache.set(f"send_emails_{request.user.id}", True)
    
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
  
  
class SendEmailView(LoginRequiredMixin, View):
    model = Email
    template_name = "user_profile/send_email.html"

    def get(self, request):
        initial_email = request.user.email if request.user.is_authenticated else ""
        send_form = SendForm(initial={"email_from": initial_email})
        return render(request, self.template_name, {"send_form": send_form})

    def post(self, request):
        selected_emails = request.POST.getlist("emails")
        to_email = ", ".join(selected_emails)

        if not selected_emails:
            messages.error(request, _("Please select at least one recipient."))
            return redirect("error_message")
        send_form = SendForm(request.POST)
        
        if send_form.is_valid():
            subject = send_form.cleaned_data["subject"]
            name_from = send_form.cleaned_data["name_from"]
            email_from = send_form.cleaned_data["email_from"]
            content = send_form.cleaned_data["content"]
            today_date = send_form.cleaned_data["today_date"]

            sent_messages = send_mail(subject, name_from, email_from, content, today_date, [to_email], fail_silently=False)
            
            if sent_messages > 0:
                return redirect("success_message")
            else:
                return redirect("error_message")
        else:
            initial_email = request.user.email if request.user.is_authenticated else ""
            send_form = SendForm(initial={"email_from": initial_email})
            return render(request, self.template_name, {"send_form": send_form, "to_email": to_email})
        

def success_message_view(request):
    return render(request, "user_profile/send_email_success.html")


def error_message_view(request):
    return render(request, "user_profile/send_email_error.html")