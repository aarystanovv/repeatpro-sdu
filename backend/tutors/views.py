
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view,permission_classes

from django_filters.rest_framework import DjangoFilterBackend
import requests

from .models import *
from .serializers import *
from .permissions import *
from .service import TutorFilter

from rest_framework.response import Response

from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.status import *
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken

class TutorRequisitesView(APIView):
    def get(self,request,tutor_id):
        try:
            tutor = TutorUser.objects.get(id = tutor_id)
            serializer =TutorRequisitesSerializer(tutor)
            return Response(serializer.data, status=status.HTTP_200_OK) 
            # # response = requests.post('http://client_service/', data=serializer.data)
            # if response.status_code == 200:
            #     return Response({'message': 'Successfully.'}, status=status.HTTP_200_OK)
        except TutorUser.DoesNotExist:
            return Response({'error':'Tutor not found'},status=status.HTTP_404_NOT_FOUND)
                
class TutorRequestView(APIView):
    def get(self, request, tutor_id):
        tutor_requests = TutorRequest.objects.filter(tutor_id=tutor_id)
        serializer = TutorRequestSerializer(tutor_requests, many=True)
        return Response(serializer.data)
    
    def patch(self, request, tutor_id):
        tutor_request_id = request.data.get('tutor_request_id')
        
        status_value = request.data.get('status')

        allowed_statuses = [choice[0] for choice in TutorRequest.STATUS_CHOICES]
        if status_value not in allowed_statuses:
            return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tutor_request = TutorRequest.objects.get(id=tutor_request_id, tutor_id=tutor_id)
        except TutorRequest.DoesNotExist:
            return Response({'error': 'Tutor request not found'}, status=status.HTTP_404_NOT_FOUND)

        tutor_request.status = status_value
        tutor_request.save()

        clients_api_url = 'http://clients-service:8000/api/'
      
        response = requests.post(clients_api_url, data=serializers.data)
        if response.status_code == 200:
            return Response({'message': 'Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ReviewCreateView(generics.CreateAPIView):
    """ Create Review for a Tutor """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(response.data, status=201)
    

class TutorsListView(generics.ListAPIView):
    """Display All Active Tutors with filter by salary,experience,degree,average rating and courses """
    queryset = TutorUser.objects.all()
    serializer_class = TutorListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    search_fields = ('id','first_name','tutorcourse__course__name','last_name','bio')
    ordering_fields = ['salary','experience']
    filterset_class = TutorFilter
    def get_queryset(self):
        return TutorUser.objects.filter(activate_post=True).annotate(average_rating=Coalesce(Avg('reviews__rating'),0.0)).order_by('-average_rating','pk')
    

class UserProfileView(APIView):
    """Display Tutor Profile """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = TutorUserProfile(user)
        return Response(serializer.data)



class TutorProfilClientView(generics.RetrieveAPIView):
    """ Display Tutor Profile for Client """
    queryset = TutorUser.objects.all()
    serializer_class = TutorUserProfile
    permission_classes = [IsAuthenticatedOrReadOnly,]
    lookup_field = 'pk'



class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    """Update Profile API"""
    serializer_class = UpdateUserSerializer
    def get_object(self):
        return self.request.user

    def put(self, request):
        user = self.get_object()
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    # permission_classes =[IsOwnerOrReadOnly,]
    

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom URL for SignIn Tutor JWT"""
    serializer_class = CustomTokenObtainPairSerializer




"""Client Service APIs"""
class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = ClientUserProfileSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = ClientUser.objects.get(email=request.user.email)
        user.avatar = request.data['avatar']
        user.save()
        return Response({'message': 'Image updated'}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        # if email is already in use
        if ClientUser.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ClientUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = ClientUser.objects.all()
        serializer = ClientUserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
