from django import forms
from .models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]

    def signup(self, req, user):
        user.nickname = self.cleaned_data['nickname']
        user.save()

LANGUAGE_CODE = 'ko'