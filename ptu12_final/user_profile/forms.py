from django.contrib.auth import get_user_model
from django import forms
from . import models
from create_scrape_send.models import AboutMe, PersonalInformation, SendScraped, Email
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = ("about_me",)


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ("picture", "first_name", "last_name", "age", "residence", "programming_languages", "hobbies", "email", "phone_number",)


class EmailForm(forms.ModelForm):
    emails = forms.ModelMultipleChoiceField(queryset=Email.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Email
        fields = ("address",)


class SendForm(forms.Form):
    subject = forms.CharField(label=_("Subject:"), max_length=200)
    name_from = forms.CharField(label=_("Name from:"), max_length=200)
    email_from = forms.EmailField(label=_("Email from:"))
    content = forms.CharField(label=_("Content:"), 
        widget=forms.Textarea(attrs={'rows': 5}),
        initial=_("""Hello, I am a 31-year-old programmer looking for a job as a junior programmer.\n
My CV: http://127.0.0.1:8000\n
Best regards D. Kaseta\n
P.S. This letter has been sent to registered companies according to the fields of activity, Computer software development, Website development, Hosting.""")
    )
    today_date = forms.DateTimeField(label=_("Today's date:"), initial=timezone.now)