from django.contrib import admin
from django.urls import path
from application.views import RegisterUserView, UserView, AllUsersView, LogoutView, TutorRequest, UserNotification, AllCourses, AllTutors, Payment, PaymentReturn
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import application.views

urlpatterns = [
    path('', AllUsersView.as_view()),
    path('user/', UserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view()),

    path('tutor/', AllTutors.as_view()),
    path('courses/', AllCourses.as_view()),
    path('tutorRequest/', TutorRequest.as_view()),
    path('notification/', UserNotification.as_view()),

    path('payment/', Payment.as_view()),
    path('payment_return/pid/', PaymentReturn.as_view())
    
]
