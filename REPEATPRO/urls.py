from django.contrib import admin
from application.views import RegisterUserView, UserView, AllUsersView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include


import application.views

urlpatterns = [
    path('user/', include('application.urls'))
]
