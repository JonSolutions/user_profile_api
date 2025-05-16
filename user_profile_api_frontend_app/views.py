from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from user_profile_api_frontend_app.forms import StudentForm, UserRegistrationForm, ProfileForm, GenderForm, \
    CourseMajorForm


def student_form_page_view(request):
    form = StudentForm()
    return render(request, '../../DjangoProject/templates/core_temps/form_page.html', {'form': form})


def course_major_view(request):
    form = CourseMajorForm()
    return render(request, 'api_frontend_temps/course_major_form.html', {'form': form})


def gender_view(request):
    form = GenderForm()
    return render(request, 'api_frontend_temps/gender_form.html', {'form': form})


def password_reset_view(request):
    form = PasswordResetForm()
    return render(request, 'api_frontend_temps/password_reset_form.html', {'form': form})


def profile_view(request):
    form = ProfileForm()
    return render(request, 'api_frontend_temps/profile_form.html', {'form': form})


def registration_view(request):
    form = UserRegistrationForm()
    return render(request, 'api_frontend_temps/registration_form.html', {'form': form})


def login_view(request):
    return render(request, 'api_frontend_temps/login.html', {})





