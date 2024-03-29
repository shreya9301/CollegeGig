from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from Account.forms import *
#from Job.permission import user_is_student
import json
import os
from collegegig.settings import MEDIA_ROOT


def get_success_url(request):
    """
        Handle success after log in
    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('Job:home')


def student_registration(request):
    """
        Handle Student Registration, Ensure that the email belongs to
        college database and is of role 'student' using email_data.json
        which represents dummy data fetched using University's API
    """
    form = StudentRegistrationForm(request.POST or None)
    if form.is_valid():
        json_file = open(os.path.join(MEDIA_ROOT, "json/email_data.json"))
        json_data = json.load(json_file)
        user_email = form.cleaned_data['email']
        if user_email in json_data['0']:
            if json_data['0'][user_email]['role'] == 'student':
                form.save()
                return redirect('Account:login')
            else:
                messages.error(request, 'You are not allowed to register as a student!')
        else:
            messages.error(request, 'You are not present in college database!')
            
    context = {
        'form': form
    }

    return render(request, 'Account/student-registration.html', context)


def faculty_registration(request):
    """
        Handle Faculty Registration, Ensure that the email belongs to
        college database and is of role 'faculty' using email_data.json
        which represents dummy data fetched using University's API
    """

    form = FacultyRegistrationForm(request.POST or None)

    if form.is_valid():
        json_file = open(os.path.join(MEDIA_ROOT, "json/email_data.json"))
        json_data = json.load(json_file)
        user_email = form.cleaned_data['email']
        if user_email in json_data['0']:
            if json_data['0'][user_email]['role'] == 'faculty':
                form.save()
                return redirect('Account:login')
            else:
                messages.error(request, 'You are not allowed to register as a faculty!')
        else:
            messages.error(request, 'You are not present in college database!')

    context = {
        'form': form
    }

    return render(request, 'Account/faculty-registration.html', context)


'''@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_student
def student_edit_profile(request, id=id):
    """
    Handle Student Profile Update Functionality
    """

    user = get_object_or_404(User, id=id)
    form = StudentProfileEditForm(request.POST or None, instance=user)

    if form.is_valid():
        form = form.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect(reverse("Account:edit-profile", kwargs={'id': form.id}))

    context = {
        'form': form
    }

    return render(request, 'Account/student-edit-profile.html', context)'''


def UserLogin(request):
    form = UserLoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            if form.is_valid():
                auth.login(request, form.get_user())
                return HttpResponseRedirect(get_success_url(request))

    context = {
        'form': form,
    }

    return render(request, 'Account/login.html', context)


def UserLogout(request):
    auth.logout(request)
    #messages.success(request, 'You are Successfully logged out')
    return redirect('Account:login')
