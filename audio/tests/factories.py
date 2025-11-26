import factory
from audio.models import Reciter
from core.tests.factories import TenantFactory

class ReciterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reciter

    tenant = factory.SubFactory(TenantFactory)
    name = factory.Sequence(lambda n: f"Reciter {n}")
    language = "ar"
    bio = factory.Faker('text')