from django.db import models


class OrganizationManager(models.Manager):

    def get_organization_by_name(self, name):
        return self.filter(name=name).first()

    def get_organization_by_uuid(self, uuid: str):
        return self.filter(uuid=uuid).first()
