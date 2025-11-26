import factory
from django.contrib.auth import get_user_model
from core.tests.factories import TenantFactory

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating User instances in tests.
    Generates unique usernames and emails using sequences.
    Automatically creates a tenant and sets password.
    """
    class Meta:
        model = User
        skip_postgeneration_save = True 
    
    tenant = factory.SubFactory(TenantFactory)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after user creation."""
        password = extracted if extracted else 'testpass123'
        self.set_password(password)
        if create:
            self.save()