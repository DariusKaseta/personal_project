from django.contrib import admin
from . import models
from .models import PersonalInformation, AboutMe
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Register your models here.

admin.site.register(models.AboutMe)


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='LT'),
        }

@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    form = PersonalInformationForm