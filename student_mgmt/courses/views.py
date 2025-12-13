from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm
from students.models import Student

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin'

def is_student(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'student'

@login_required
@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
@user_passes_test(is_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add Course'})

@login_required
@user_passes_test(is_admin)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            if 'logo' not in request.FILES:
                form.instance.logo = course.logo
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('courses:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

@login_required
@user_passes_test(is_admin)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('courses:course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
@user_passes_test(is_admin)
def assign_course(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            student = enrollment.student
            course = enrollment.course
            
            messages.success(request, f'Course assigned successfully to {student.user.email}.')
            
            return redirect('courses:course_list')
    else:
        form = EnrollmentForm()
    return render(request, 'courses/assign_course.html', {'form': form})

@login_required
def my_courses(request):
    if hasattr(request.user, 'student'):
        enrollments = Enrollment.objects.filter(student=request.user.student)
        return render(request, 'courses/my_courses.html', {'enrollments': enrollments})
    else:
        messages.error(request, 'You are not a student.')
        return redirect('accounts:dashboard')
