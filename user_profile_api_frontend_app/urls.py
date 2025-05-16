from django.urls import path

from user_profile_api_frontend_app import views

urlpatterns = [
    path('user-page/', views.student_form_page_view, name='user-page'),
    path('registration/', views.registration_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('gender/', views.gender_view, name='gender'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('course/', views.course_major_view, name='course'),
    path('profile/', views.profile_view, name='profile'),
]