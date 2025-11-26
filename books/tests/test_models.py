import pytest
from books.models import Book
from books.tests.factories import BookFactory
from core.tests.factories import TenantFactory

class TestBookModel:
    """
    Unit tests for Book model.
    Tests cover model creation, tenant association, unique constraints, and relationships.
    """
    
    @pytest.mark.django_db
    def test_create_book(self):
        """
        Test successful creation of a Book instance.
        Verifies that all required fields are properly set and saved to the database.
        """
        book = BookFactory()
        assert book.id is not None
        assert book.title is not None
        assert book.tenant is not None
        assert book.language == "ar"
    
    @pytest.mark.django_db
    def test_book_belongs_to_tenant(self):
        """
        Test that book is correctly associated with a tenant.
        Verifies the ForeignKey relationship between Book and Tenant.
        """
        tenant = TenantFactory(domain="test")
        book = BookFactory(tenant=tenant)
        assert book.tenant == tenant
        assert book.tenant.domain == "test"
    
    @pytest.mark.django_db
    def test_book_str(self):
        """
        Test the __str__ method of the Book model.
        Verifies that string representation returns the book's title.
        """
        book = BookFactory(title="Test Book")
        assert str(book) == "Test Book"
    
    @pytest.mark.django_db
    def test_unique_title_per_tenant(self):
        """
        Test unique constraint: same title can exist in different tenants.
        Verifies that two books with the same title can exist 
        if they belong to different tenants.
        """
        tenant1 = TenantFactory(domain="tenant1")
        tenant2 = TenantFactory(domain="tenant2")
        
        book1 = BookFactory(tenant=tenant1, title="Same Title")
        book2 = BookFactory(tenant=tenant2, title="Same Title")
        
        assert book1.title == book2.title
        assert book1.tenant != book2.tenant
    
    @pytest.mark.django_db
    def test_unique_title_same_tenant_fails(self):
        """
        Test that creating two books with the same title in the same tenant raises an exception.
        Verifies the unique_together constraint ('tenant', 'title').
        """
        tenant = TenantFactory()
        BookFactory(tenant=tenant, title="Unique Title")
        
        with pytest.raises(Exception):
            BookFactory(tenant=tenant, title="Unique Title")