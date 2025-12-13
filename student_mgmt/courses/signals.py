from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Enrollment

@receiver(post_save, sender=Enrollment)
def send_course_assignment_email(sender, instance, created, **kwargs):
    if created:  # Only send when a new enrollment is created
        student = instance.student
        course = instance.course
        
        subject = f"You have been enrolled in {course.title}"
        message = (
            f"Hello {student.user.first_name},\n\n"
            f"You have been successfully enrolled in the course: {course.title}.\n\n"
            f"Description:\n{course.description}\n\n"
            "Best regards,\n"
            "Student Management System"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.user.email],
            fail_silently=False,
        )
