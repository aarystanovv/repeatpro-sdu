from django_filters import  rest_framework as filters
from .models import *


class TutorFilter(filters.FilterSet):
    salary =filters.RangeFilter( label='Price per lesson')
    experience = filters.RangeFilter(label='Enter experience range (0-10)')
    degree = filters.ChoiceFilter(choices=TutorUser.DEGREE_CHOICES,label = f'Сhoose a tutor by degree',empty_label="Degrees")
    # rating = filters.NumberFilter( method='filter_by_rating')
    rating = filters.ChoiceFilter(choices=Review.RATING_CHOICES,method='filter_by_rating',label = 'Choose a rating',empty_label="Ratings")
    course = filters.ModelMultipleChoiceFilter(
        queryset=Courses.objects.all(),
        field_name='tutorcourse__course__id',
        to_field_name='id',label = 'Choose courses'
    )

    class Meta:
        model = TutorUser
        fields = ('salary', 'experience', 'degree','rating','course')

    def filter_by_rating(self, queryset, name, value):
        queryset = queryset.annotate(average_rating=models.Avg('reviews__rating'))
        queryset = queryset.filter(average_rating__gte=(value))
        return queryset
    
 

    