from django.db import models # type: ignore 
from django.contrib.auth.models import User # type: ignore
from django.utils import timezone  # type: ignore

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
    start_time = models.CharField(max_length=255)
    days = models.JSONField(default=list)

    class Meta:
        unique_together = ['user', 'course_number', 'section_number'] # Cant sign up for the same class twice

    def __str__(self):
        return f"{self.class_name} ({self.course_number}-{self.section_number})"


class ClassTradeRequest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', default=None)
    owner_student_id = models.CharField(max_length=20, default="-1")  
    offered_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='offered_requests')
    desired_class_number = models.CharField(max_length=100, default="Unknown")
    desired_section_number = models.CharField(max_length=10, default="-1")
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open')
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_requests', blank=True)
    downvoted_by = models.ManyToManyField(User, related_name='downvoted_requests', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_requests', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Request {self.id} - {self.offered_class.class_name} for {self.desired_class_number}-{self.desired_section_number}"
