from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student
from .forms import StudentForm
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin'

@login_required
@user_passes_test(is_admin)
def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.all()
    
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(roll_number__icontains=query)
        )
    
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/student_list.html', {'page_obj': page_obj, 'query': query})

@login_required
@user_passes_test(is_admin)
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # We need to create a User manually or expect one selected?
            # Requirement says "Add student". Logic usually implies creating a user too.
            # But here we might just link to existing user or create one.
            # To simplify, we'll create a dummy user or expect user creation logic.
            # For this "complete SMS", let's assume we create a user with default password 'password123'
            # and username as roll_number for simplicity, or we should have a combined form.
            # The Form above updates user, but save() expects instance.pk for update.
            # Let's handle creation:
            
            username = form.cleaned_data['roll_number']
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Student with Roll Number {username} already exists.')
                return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})
            
            user = User.objects.create_user(
                username=username, 
                password='password123',
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # The post_save signal on User creates a Student instance.
            # We need to update that instance instead of creating a new one.
            if hasattr(user, 'student'):
                student = user.student
                form = StudentForm(request.POST, request.FILES, instance=student)
                if form.is_valid():
                    form.save()
            else:
                student = form.save(commit=False)
                student.user = user
                student.save()
            messages.success(request, 'Student created successfully. Login with Roll No & password123')
            return redirect('students:student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
@user_passes_test(is_admin)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})

@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete() # Delete associated user too
        messages.success(request, 'Student deleted successfully.')
        return redirect('students:student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
