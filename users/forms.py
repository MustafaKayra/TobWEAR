from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Şifre'}), label="Şifre")
    password2 = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Şifreyi Onayla'}), label="Şifre")
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'adress', 'city', 'country', 'zipcode', 'gsmnumber', 'cardnumber', 'cardexpire', 'cvc')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['adress', 'city', 'country', 'zipcode', 'gsmnumber', 'cardnumber', 'cardexpire', 'cvc']:
            self.fields[field].required = False


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Şifreler Uyuşmuyor!")
        return cleaned_data
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'placeholder': 'Email Giriniz'}))
    password = forms.CharField(label="Şifre",widget=forms.PasswordInput(attrs={'placeholder': 'Şifre'}))
    password2 = forms.CharField(label="Şifreyi Onayla",widget=forms.PasswordInput(attrs={'placeholder': 'Şifreyi Onayla'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError("Şifreler Uyuşmuyor!")
        return cleaned_data