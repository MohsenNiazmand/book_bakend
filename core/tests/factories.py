import factory
from core.models import Tenant

class TenantFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating Tenant instances in tests.
    Generates unique names and domains using sequences to avoid conflicts.
    Sets is_active=True by default for active tenants.
    """
    class Meta:
        model = Tenant
    
    name = factory.Sequence(lambda n: f"Tenant {n}")
    domain = factory.Sequence(lambda n: f"tenant{n}")
    is_active = True