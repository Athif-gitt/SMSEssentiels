from django import forms
from .models import Course, Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
