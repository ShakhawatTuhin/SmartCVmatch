from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    parsed_text = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f"Resume {self.id}"
    

from django.contrib.postgres.fields import ArrayField  # At the top

skills = ArrayField(models.CharField(max_length=100), blank=True, null=True)