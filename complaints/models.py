from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Complaint category e.g. Road, Water, Electricity, Garbage, Drainage"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    complaint_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="Area / street name")
    photo = models.ImageField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    resolution_photo = models.ImageField(upload_to='resolved/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.complaint_id:
            # simple readable ID e.g. CF-2026-0001, finalized after first save for the PK
            super().save(*args, **kwargs)
            self.complaint_id = f"CF-{self.created_at.year}-{self.pk:04d}"
            super().save(update_fields=['complaint_id'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} - {self.title}"

    class Meta:
        ordering = ['-created_at']
