from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, firstname, lastname, age, phone, gender,  password=None):
        if not email:
            raise ValueError('Users must have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname, lastname=lastname, age=age, phone=phone, gender=gender)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password):
        user = self.create_user(email, firstname, lastname, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255, unique=True)
    lastname = models.CharField(max_length=255, unique=True)
    avatar = models.URLField(blank=True, null=True)

    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)
    rating = models.FloatField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tutor_id = models.IntegerField()
    status = models.CharField(max_length=50)
    text = models.TextField()
    link = models.CharField(max_length=255)
    price = models.IntegerField()


class PaymentAccounts(models.Model):
    payment_id = models.IntegerField()
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tutor_id = models.IntegerField()
    status = models.CharField(max_length=50)


