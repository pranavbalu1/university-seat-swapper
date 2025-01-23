from django.db import models # type: ignore 
from django.contrib.auth.models import User # type: ignore

# Extend the User model for additional profile data
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=100, unique=True)  # Unique student ID
    full_name = models.CharField(max_length=255)
    email = models.EmailField(default='default@example.com')

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


# Class model to store the details of classes a student is enrolled in
class StudentClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')
    course_number = models.CharField(max_length=100)
    section_number = models.CharField(max_length=10)
    class_name = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.class_name} ({self.course_number}-{self.section_number})"
