from django.contrib.auth import get_user_model
from django import forms
from . import models
from create_scrape_send.models import AboutMe, PersonalInformation, SendScraped, Email
from django.utils import timezone



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
    subject = forms.CharField(max_length=200)
    name_from = forms.CharField(max_length=200)
    email_from = forms.EmailField()
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        initial="""Hello, I am a 31-year-old programmer looking for a job as a junior programmer.\n My CV: http://127.0.0.1:8000\n P.S. This letter has been sent to registered companies according to the fields of activity, Computer software development, website development, hosting."""
    )
    today_date = forms.DateTimeField(initial=timezone.now)