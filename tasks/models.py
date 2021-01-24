from django.db import models

class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']