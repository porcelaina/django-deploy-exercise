from django.shortcuts import render
from basic_app5.forms import UserForm, UserProfileInfoForm

# from django.core.urlresolvers import reverse -> 에러남! Django 2.0 replaced django.core.urlresolvers with django.urls.
# https://github.com/mgrp/django-distill/issues/7

from django.urls import reverse
from django.contrib.auth.decorators import login_required  # Super awesome!!!
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return render(request, 'basic_app5/index.html')


def register(request):

    registered = False

    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # 사용자로부터 받은 입력을 바로 저장하는경우는 commit=False 필요없이 바로 save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False) # 사용자로부터 받은 입력을 바로 저장하는것이 아닌 경우는 commit=False를 주고 필요한 처리를 한후 나중에 save()
            profile.user = user # model에서의 User와 UserProfileInfo 의 one-to-one relationship을 정의해주는 line. 여기의 user는 forms.py 의 UserForm 임.

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request, 'basic_app5/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})


def user_login(request): # 함수이름을 login 으로 하면 Django 내장모듈을 override 하게 되어 에러남.

    if request.method=="POST":
        username = request.POST.get('username') # 여기의 'username' 은 login.html 에서 input으로 받는 username임.
        password = request.POST.get('password') # 여기도 마찬가지로 login.html에서 받는것

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index')) # login 성공하면 사용자를 index 페이지로 다시 보냄.

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username = {} and password = {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'basic_app5/login.html', {})


#decorator 이용

@login_required
def user_logout(request):
    logout(request) # 내장된 logout function
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You are logged in!")