from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from djoser.serializers import UserCreateSerializer
from django.forms import *


class TutorRequisitesSerializer(serializers.ModelSerializer):
    """Tutor Requisites"""
    class Meta:
        model=TutorUser
        fields = ('id','email','first_name','last_name','phone_number')


class TutorRequestSerializer(serializers.ModelSerializer):
    """Tutor Requests list for Accept/Reject"""
    client = serializers.CharField(source = 'client.get_full_name')
    class Meta:
        model=TutorRequest
        fields = ("id","client","status","text","date_time",)



class ClientUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('id', 'email', 'username', 'password', 'avatar', 'age', 'gender', 'phone', 'rating')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = ClientUser.objects.create_user(**validated_data)
        return user


    
class TutorUserCreateSerializer(UserCreateSerializer):
    """ Tutor Sign Up using Djoser JWT """
    class Meta(UserCreateSerializer.Meta):
        model = TutorUser
        fields = ('id','email','first_name','last_name','phone_number','password')



class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Create Review for a Tutor """
    client = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'

    def get_default_tutor(self):
        tutor_id = self.context.get('view').kwargs.get('tutor_id')
        try:
            return TutorUser.objects.get(id=tutor_id)
        except TutorUser.DoesNotExist:
            raise serializers.ValidationError("Tutor not found.")
    def create(self, validated_data):
        tutor = validated_data.pop('tutor')
        review = Review.objects.create(tutor=tutor, **validated_data)
        return review        

class ReviewViewSerializer(serializers.ModelSerializer):
    """ Display All Tutor Reviews """    
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    class Meta:
        model = Review
        fields = ('client_name','description','rating','created_at')

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class TutorUserProfile(serializers.ModelSerializer):
    """ Display Tutor Profile for Client """
    def get_average_rating(self, tutor):
        reviews = tutor.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(),2) if reviews.count() > 0 else 0.0

    average_rating = serializers.SerializerMethodField('get_average_rating')
    reviews = ReviewViewSerializer(many=True,read_only=True)
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        return [course.name for course in obj.courses.all()]
    class Meta:
        model = TutorUser
        fields = ('first_name','last_name','email','phone_number','bio','avatar','files','date_of_birth','experience','education','degree','courses','yof','salary','link','average_rating','reviews')


class UpdateUserSerializer(serializers.ModelSerializer):
        """ Update Tutor Profile """
        tutor_user_model=TutorUser
        def getEmail(self, tutor_user_model):
            return tutor_user_model.email
        def getFirstName(self, tutor_user_model):
            return tutor_user_model.first_name
        def getLastName(self, tutor_user_model):
            return tutor_user_model.last_name
        def getPhone(self, tutor_user_model):
            return tutor_user_model.phone_number
        def getCourses(self, tutor_user_model):
            return tutor_user_model.courses
        
        email = serializers.SerializerMethodField("getEmail")
        first_name = serializers.SerializerMethodField("getFirstName")
        last_name = serializers.SerializerMethodField("getLastName")
        phone_num = serializers.SerializerMethodField("getPhone")

        courses = serializers.SlugRelatedField(
            queryset=Courses.objects.all(),
            many=True,
            slug_field='name',
            required=False
        )
        class Meta:
            model = TutorUser
            fields = ('email','first_name','last_name','phone_num',"avatar",'bio','date_of_birth','experience','education','degree','yof','courses','salary','files','link','activate_post')
        
        
        def update(self, instance, validated_data):
            courses_data = validated_data.pop('courses', None)
            for attr, value in validated_data.items():
                if value is not None and getattr(instance, attr) != value:
                    setattr(instance, attr, value)
            if courses_data is not None:
                instance.courses.set(courses_data)
            instance.save()
            return instance

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            courses = instance.courses.all()
            course_names = [course.name for course in courses]
            representation['courses'] = course_names
            return representation
        


class TutorListSerializer(serializers.ModelSerializer):
    """Display All Active Tutors """
    courses = serializers.SerializerMethodField()
    def get_courses(self, obj):
        return [course.name for course in obj.courses.all()]
    def get_average_rating(self, tutor):
        reviews = tutor.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(),2) if reviews.count() > 0 else 0.0
    average_rating = serializers.SerializerMethodField('get_average_rating')

    class Meta:
        model = TutorUser
        fields = ('id','first_name','last_name','bio','salary','avatar','average_rating','experience','courses')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom URL for SignIn Tutor JWT """
    def validate(self, attrs):
        data = super().validate(attrs)
        return data     