from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User, Group
from organization.managers import OrganizationManager, TaskManager
from django_celery_beat.models import PeriodicTask, ClockedSchedule
import json
from datetime import timedelta


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
        permissions = [
            ("create_project", "Can create project"),
            ("read_project", "Can read project"),
        ]

    def __str__(self):
        return self.name


class Project(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Task Name')
    description = models.TextField(null=True, blank=True, verbose_name='Task Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    periodic_task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def setup_task(self):
        self.periodic_task = PeriodicTask.objects.create(
            name=self.name,
            task='notify_task',
            args=json.dumps([self.user.email, self.name]),
            one_off=True,
            clocked=ClockedSchedule.objects.create(
                clocked_time=self.expiry_date - timedelta(hours=1, minutes=1)
            )
        )
        self.save()

    objects = TaskManager()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['created_at']

    def __str__(self):
        return self.name
