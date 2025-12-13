from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.course_create, name='course_create'),
    path('<int:pk>/edit/', views.course_update, name='course_update'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('assign/', views.assign_course, name='assign_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
