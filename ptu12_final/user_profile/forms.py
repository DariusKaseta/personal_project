from django.contrib.auth import get_user_model
from django import forms
from . import models
from create_scrape_send.models import AboutMe, PersonalInformation
from django.forms import inlineformset_factory


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = ("about_me",)

class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ("picture", "first_name", "last_name", "age", "residence", "programming_languages", "hobbies", "email", "phone_number",)
