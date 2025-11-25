from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Tenant

class User(AbstractUser):
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        unique_together = ('tenant', 'username')

    def __str__(self):
        return self.username