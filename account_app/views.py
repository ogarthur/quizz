from django.shortcuts import render
from . import forms
from django.utils.translation import gettext as _
#
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .forms import CustomUserCreationForm

from django.contrib.auth.models import User
import random, string
app_name = 'account_app'
# Create your views here.


# #################USER##################



def register(request):
    registered = False
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

            return redirect('index')
        else:
            print(user_form.errors)
            return render(request, '{}/registration.html'.format(app_name),
                          {'user_form': user_form,
                           'registered': registered})
    else:
        user_form = CustomUserCreationForm()
        return render(request, '{}/registration.html'.format(app_name), {'user_form': user_form,'registered': registered})


#LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')

            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} ".format(username))
            return render(request, '{}/login.html'.format(app_name), {'login_error': 'Credeenciales no válidos'})
    else:
        return render(request, '{}/login.html'.format(app_name), {})


# LOGOUT
@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def delete_user(request):
    from django.contrib.auth.models import User
    user = User.objects.get(username=request.user.username)
    user.delete()
    logout(request)
    return redirect('index')


@login_required
def get_profile(request, user_id):
    user = User.objects.get(id=user_id)

    user_data = {
        'user': user,

    }
    return render(request, '{}/userProfile.html'.format(app_name), {'user_data': user_data})

