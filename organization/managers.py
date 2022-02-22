from django.db import models


class OrganizationManager(models.Manager):

    def get_organization_by_name(self, name):
        return self.filter(name=name).first()

    def get_organization_by_uuid(self, uuid: str):
        return self.filter(uuid=uuid).first()


class TaskManager(models.Manager):

    def get_tasks_by_user(self, user):
        return self.filter(user=user)

    def get_task_by_uuid(self, uuid: str):
        return self.filter(uuid=uuid).first()

    def get_tasks_by_organization(self, organization):
        return self.filter(organization=organization)
