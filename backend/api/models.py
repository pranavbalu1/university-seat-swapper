from django.db import models

class Class(models.Model):
    course_number = models.CharField(max_length=10)
    section_number = models.CharField(max_length=5)
    instructor = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    class_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.class_name} ({self.course_number})"

class SeatExchange(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class_offered = models.ForeignKey(Class, related_name='offered_classes', on_delete=models.CASCADE)
    class_requested = models.ForeignKey(Class, related_name='requested_classes', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} offering {self.class_offered.class_name} for {self.class_requested}"
