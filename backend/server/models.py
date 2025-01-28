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
    start_time = models.CharField(max_length=255)
    days = models.JSONField(default=list)

    class Meta:
        unique_together = ['user', 'course_number', 'section_number'] # Cant sign up for the same class twice

    def __str__(self):
        return f"{self.class_name} ({self.course_number}-{self.section_number})"


class ClassTradeRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trade_requests")
    offered_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name="offered_class")
    requested_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name="requested_class")
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('accepted', 'Accepted'), ('closed', 'Closed')], default='open')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    favorites = models.ManyToManyField(User, related_name='favorite_requests', blank=True)

    def __str__(self):
        return f"Request by {self.requester.username} ({self.status})"

class AcceptedRequest(models.Model):
    request = models.OneToOneField(ClassTradeRequest, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_requests')

    def __str__(self):
        return f"Accepted by {self.accepted_by.username}"
