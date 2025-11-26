import factory
from books.models import Book
from core.tests.factories import TenantFactory

class BookFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating Book instances in tests.
    Generates unique titles using sequences and sets default language to 'ar'.
    Automatically creates a tenant for each book.
    """
    class Meta:
        model = Book
    
    tenant = factory.SubFactory(TenantFactory)
    title = factory.Sequence(lambda n: f"Book {n}")
    description = "Test description"
    language = "ar"