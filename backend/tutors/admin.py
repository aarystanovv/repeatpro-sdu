from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Here you have to import the User model from your app!
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin



admin.site.register(TutorUser)
admin.site.register(ClientUser)
admin.site.register(Review)
admin.site.register(Courses)
admin.site.register(TutorCourse)

admin.site.register(TutorRequest)

