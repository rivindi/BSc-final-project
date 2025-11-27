from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=50)
    message = forms.CharField(max_length=500)

    def get_message(self):
        return f"""Name: {self.cleaned_data.get("name")}
Email: {self.cleaned_data.get("email")}
Subject: {self.cleaned_data.get("subject")}
Message: {self.cleaned_data.get("message")}
        """

    def send_mail(self):
        send_mail(
            "New message reqeust",
            self.get_message(),
            settings.EMAIL_HOST_USER,
            [
                settings.EMAIL_HOST_USER,
            ],
            fail_silently=False,
        )
