from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, logout as d_logout, login as d_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from .forms import *
from .models import Profile


def status_response(status, message):
    return JsonResponse({'status': status, 'message': message})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            # if it is email
            if '@' in cdata['username']:
                try:
                    user = User.objects.get(email__iexact=cdata['username'])
                except User.DoesNotExist:
                    return status_response(False, {'email': 'Login or password is wrong!!'})
            else:
                try:
                    user = User.objects.get(username__exact=cdata['username'])
                except User.DoesNotExist:
                    return status_response(False, {'email': 'Login or password is wrong!!'})

            user = authenticate(username=user.username, password=cdata['password'])
            if user is not None:
                d_login(request, user)
                return status_response(True, '/')
            else:
                return status_response(False, {'login': 'Login or password is wrong!!'})
        else:
            return status_response(False, form.errors)

    return render(request, 'login.html', {'next': next})


@login_required
def logout(request):
    d_logout(request)
    return redirect(reverse('index'))


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            d_login(request, user)
            return status_response(True, '/')
        else:
            return status_response(False, form.errors)

    return render(request, 'signup.html')


@login_required(login_url='/login/')
def profile(request):
    profile = Profile.objects.get(user_id__exact=request.user.pk)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html', {'user': profile.user})
        else:
            return render(request, 'profile.html', {
                        'user': profile.user,
                        'errors': form.errors
                        })
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return status_response(True, 'Password was successfully changed.')
        else:
            return status_response(False, form.errors)


@login_required
def logout(request):
    d_logout(request)
    return redirect(reverse('index'))
