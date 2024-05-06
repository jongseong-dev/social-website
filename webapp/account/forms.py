from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        is_empty = cd.get("password") is None or cd.get("password2") is None
        is_sync = cd.get("password") == cd.get("password2")
        if is_empty or not is_sync:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]
