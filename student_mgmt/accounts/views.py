from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Profile
from courses.models import Enrollment
# from django.core.mail import send_mail
# from django.http import HttpResponse
# from django.conf import settings

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update role in profile
            role = form.cleaned_data.get('role')
            user.profile.role = role
            user.profile.save()
            
            messages.success(request, 'Registration successful. Please login.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # name = user.first_name
                # user.courses = Enrollment.objects.filter(student=name)
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    profile = request.user.profile
    if profile.role == 'admin':
        return render(request, 'accounts/admin_dashboard.html')
    else:
        return render(request, 'accounts/student_dashboard.html')
    
# def test_email(request):
#     try:
#         send_mail(
#             subject="Django Email Test",
#             message="If you received this email, SMTP is working!",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[settings.EMAIL_HOST_USER],
#             fail_silently=False,
#         )
#         return HttpResponse("✅ Test email sent successfully!")
#     except Exception as e:
#         return HttpResponse(f"❌ Error: {e}")

