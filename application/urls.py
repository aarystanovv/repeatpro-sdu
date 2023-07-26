from django.contrib import admin
from django.urls import path, include
from application.views import RegisterUserView, UserView, AllUsersView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import application.views

urlpatterns = [
    path('', AllUsersView.as_view()),
    path('auth/', include('rest_framework.urls')),
    path('user/', UserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view())
]
