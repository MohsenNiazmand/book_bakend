from django.db import models
from django.db.models import Manager, QuerySet

class TenantQuerySet(QuerySet):
    """QuerySet that filters by current tenant"""
    def for_tenant(self, tenant):
        if tenant:
            return self.filter(tenant=tenant)
        return self.none()

class TenantManager(Manager):
    """Manager that automatically filters by tenant"""
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)
    
    def for_tenant(self, tenant):
        return self.get_queryset().for_tenant(tenant)

class Tenant(models.Model):
    """Tenant model for multitenancy"""
    name = models.CharField(max_length=255, unique=True)
    domain = models.CharField(max_length=255, unique=True, help_text="Domain or subdomain identifier")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
