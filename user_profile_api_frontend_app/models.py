import uuid

from django.db import models

from user_profile_api_app.models import User


# Create your models here.
class GenderModel(models.Model):
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.gender}'

class CourseMajorModel(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course_name} ({self.course_code})'

class PasswordResetModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.reset_id}'
