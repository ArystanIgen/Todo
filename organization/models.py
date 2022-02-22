from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User, Group
from organization.managers import OrganizationManager


class Organization(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Organization Name')
    address = models.TextField(null=True, blank=True, verbose_name='Organization Address')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Organization City')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Organization Country')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrganizationManager()

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=f"tsk_{uuid4()}", editable=False)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Task Name')
    description = models.TextField(null=True, blank=True, verbose_name='Task Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['created_at']

    def __str__(self):
        return self.name
