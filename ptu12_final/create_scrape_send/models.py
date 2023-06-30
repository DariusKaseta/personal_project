from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

User = get_user_model()


class PersonalInformation(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), related_name = "personal_informations", on_delete=models.CASCADE)
    picture = models.ImageField(_("picture"), upload_to="ptu12_final/media/", null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    age = models.IntegerField(_("age"))
    residence = models.CharField(_("residence"), max_length=50, db_index=True)
    programming_languages = models.TextField(_("programming languages"), max_length=4000)
    hobbies = models.CharField(_("hobbies"), max_length=200, null=True, blank=True)
    email = models.CharField(_("email"), max_length=100, db_index=True)
    phone_regex = RegexValidator(regex=r'^\+370\d{8}$', message="Phone number must be in the format: '+370XXXXXXXX'. Up to 11 digits are allowed.")
    phone_number = PhoneNumberField(validators=[phone_regex], null=False, blank=False, unique=True)

    class Meta:
        verbose_name = _("personal information")
        verbose_name_plural = _("personal informations")

    def __str__(self):
        return f"{self.residence} - {self.programming_languages} - {self.phone_number}"

    def get_absolute_url(self):
        return reverse("personalinformation_detail", kwargs={"pk": self.pk})


class AboutMe(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), related_name= "about_mes", on_delete=models.CASCADE)
    personal_information = models.ForeignKey(PersonalInformation, verbose_name=_("personal information"), on_delete=models.CASCADE)
    about_me = models.TextField(_("about me"), max_length=4000, null=True, blank=True)

    class Meta:
        verbose_name = _("about me")
        verbose_name_plural = _("about mes")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("aboutme_detail", kwargs={"pk": self.pk})
    



    

