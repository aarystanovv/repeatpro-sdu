
from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views

from djoser import views
from djoser.views import UserViewSet,TokenCreateView
from django.conf.urls.static import static



from tutors.views import *

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView
)
router = DefaultRouter()
# router.register(r'auth/tutors', CustomTokenObtainPairViewSet, basename='custom_token_obtain_pair')


urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include('tutors.urls')),
    path('', include(router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),

    path('signup/tutor/', UserViewSet.as_view({'post': 'create'}), name='tutor_signup'),
    path('signin/tutor/', CustomTokenObtainPairView.as_view(), name='tutor_signin'),
    
    path('tutors/', TutorsListView.as_view(), name='tutors_list'),
    path('tutor-profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('tutor-profile/', UserProfileView.as_view(), name='tutor-profile'),
    path('tutors/<int:pk>/',TutorProfilClientView.as_view(), name='tutor_page'),
    
    path('tutor/<int:pk>/review/', ReviewCreateView.as_view(), name='review_page'),
    path('tutor_requests/<int:tutor_id>/', TutorRequestView.as_view(), name='tutor_requests'),
    path('tutors/<int:tutor_id>/requisites/', TutorRequisitesView.as_view(),name='tutor_requisites'),



    path('', AllUsersView.as_view()),
    path('user/', UserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view())

]



urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

