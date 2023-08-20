from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db.models import Avg
from django.utils import timezone
from django.core.validators import RegexValidator
from datetime import time, timedelta


from django.contrib.auth.models import BaseUserManager
from multiselectfield import *
from rest_framework.exceptions import ValidationError

def validate_courses(value):
    if value.count()==0:
        raise ValidationError("At least one course must be selected.")





class Courses(models.Model):
    name = models.CharField('Course name',max_length=100)

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name



class ClientUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class TutorUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email is not given!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email,password,**extra_fields)
    

class TutorUser(AbstractBaseUser, PermissionsMixin):
    EXPERIENCE_CHOICES = (
            (0, 'Менее 1 года'),
            (1, 'Более 1 года'),
            (2, 'Более 2 лет'),
            (3, 'Более 3 лет'),
            (5, 'Более 5 лет'),
            (10, 'Более 10 лет'),
    )

    SALARY_CHOICES = (
        (1000, '1000 тнг/час'),
        (2000, '2000 тнг/час'),
        (3000, '3000 тнг/час'),
        (4000, '4000 тнг/час'),
        (5000, '5000 тнг/час'),
        (6000, '6000 тнг/час'),
        (7000, '7000 тнг/час'),
        (8000, '8000 тнг/час'),
        (9000, '9000 тнг/час'),
        (10000, '10000 тнг/час'),
        (11000, '11000 тнг/час'),
    )

    DEGREE_CHOICES = (
        ('st','Студент'),
        ('bch','Бакалавр'),
        ("mg",'Магистр'),
        ("phd",'Кандидат Наук'),
        ("pf",'Профессор')
    )
   


    def positive_validator(value):
        if value <= 0:
            raise ValidationError("Field must be a positive number.")

    
    email = models.EmailField('Email',max_length=255, unique=True)
    password = models.CharField('Password',max_length=128, null=True)
    first_name = models.CharField('First Name',max_length=255, blank=False, null=False)
    last_name = models.CharField('Last name',max_length=255, blank=False, null=False)
    created_at = models.DateTimeField('Created at',auto_now_add=True)
    updated_at = models.DateTimeField('Updated at',auto_now=True)
    phone_number = models.CharField('Phone Num',max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField('About Me',max_length=2000, blank=True, null=True)
    date_of_birth = models.DateField('Date of Birth',null=True, blank=True)
    experience = models.IntegerField('Experience',max_length=20, null=True, blank=True,choices=EXPERIENCE_CHOICES)
    education = models.CharField('Education/University',max_length=255, null=True, blank=True)
    degree = models.CharField('Academic Degree',max_length=255,null=True,blank=True,choices=DEGREE_CHOICES)
    yof = models.IntegerField('Year of Ending ',blank=True, null=True,validators=[positive_validator])
    avatar = models.ImageField('Profile Avatar',upload_to='tutor_avatars/', default='tutor_avatars/tutor_avatar_def.png')
    files = models.FileField('Files',upload_to='fmedia\\files/%Y/%m/%d',null=True, blank=True)
    salary = models.IntegerField('Salary',max_length=200,null=True, blank=True, choices=SALARY_CHOICES)
    link = models.URLField('Video Link',blank=True, null=True)
    activate_post = models.BooleanField('Acticate Profile',default=True)

    courses = models.ManyToManyField(Courses,through='TutorCourse',validators=[validate_courses])


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' ,'phone_number']
    objects = TutorUserManager()


    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='tutor_users'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='titor_users'
    )

    def get_full_name(self):
        return f"{self.courses}"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'




class ClientUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    avatar = models.URLField(blank=True, null=True)

    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)
    rating = models.FloatField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ClientUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='client_users'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='client_users'
    )

    def get_full_name(self):
        return f"{self.username}"
    def __str__(self):
        return f'{self.email}'
    

class Review(models.Model):
    RATING_CHOICES=(
        (1,'1 star' ),
        (2,'2 stars' ),
        (3,'3 stars' ),
        (4,'4 stars' ),
        (5,'5 stars' ),
    )
    tutor = models.ForeignKey(TutorUser,on_delete=models.CASCADE,related_name = 'reviews')
    client = models.ForeignKey(ClientUser,on_delete=models.CASCADE,related_name='reviewer',default=None)
    description = models.TextField(max_length=500,null=True)
    rating = models.PositiveIntegerField('Rating',choices=RATING_CHOICES,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    class Meta:
        unique_together=('tutor','client',)

    def __str__(self):
        return f"Review by {self.client.get_full_name()} for Tutor {self.tutor}"




class TutorCourse(models.Model):
    tutor = models.ForeignKey(TutorUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,validators=[validate_courses])

    def __str__(self):
        return f'{self.tutor.first_name} - {self.course.name}'



class TutorRequest(models.Model):

    STATUS_CHOICES = (
        ('Accepted','Accept Request'),
        ('Rejected','Reject Request'),
        ('Pending','Pending'),
    )
  
    tutor = models.ForeignKey(TutorUser, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientUser,on_delete=models.CASCADE,default=None)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending',blank=True,null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return f'{self.client.pk} request for Tutor - {self.tutor.first_name} {self.tutor.last_name}'



class Payment(models.Model):
    tutor = models.ForeignKey(TutorUser, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

