from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Course
from .serializer import CourseSerializer
from rest_framework.permissions import IsAuthenticated


class CourseAPIList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

#Возвращает список Курсов по get запросу и добавляет новые курсы по post запросу