from django.urls import path
from . import views


urlpatterns = [
    #api urls
    path('register/', views.register_user, name='register'),
    path('token/', views.get_auth_token, name='token'),
    path('profiles/', views.ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    path('my-profile/', views.MyProfileView.as_view(), name='my-profile'),

]