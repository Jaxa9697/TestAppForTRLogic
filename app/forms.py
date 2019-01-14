from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField()
    login = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    birthday = forms.DateField(required=False)
    about = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Profile
        fields = ['birthday', 'about', 'avatar']

    def save(self, commit=True):
        obj = super().save(commit=False)
        user = User.objects.get(profile=obj)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['login']

        if commit:
            user.save()
            obj.save()

        return obj


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data['email'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count():
            raise forms.ValidationError('User with this email address already exist')
        else:
            return self.cleaned_data['email']

    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            Profile(user=obj).save()

        return obj
