from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    parsed_text = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f"Resume {self.id}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_company = models.CharField(max_length=255)
    job_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.job_title} at {self.job_company}"

from django.contrib.postgres.fields import ArrayField  # At the top

skills = ArrayField(models.CharField(max_length=100), blank=True, null=True)