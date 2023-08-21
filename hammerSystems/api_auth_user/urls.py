from django.contrib import admin
from django.urls import path

from .views import VerificationUser, SignIn, logout_user, ProfileUser

app_name = 'api_auth_user'

urlpatterns = [
    path('', VerificationUser.as_view(), name='verification_user'),
    path('login/', SignIn.as_view(), name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('profile/', ProfileUser.as_view(), name='profile_user')
]
