import pytest
from django.core.exceptions import ValidationError
from core.models import Tenant
from core.tests.factories import TenantFactory

class TestTenantModel:
    """
    Unit tests for Tenant model.
    Tests cover model creation, string representation, and unique constraints.
    """
    
    @pytest.mark.django_db
    def test_create_tenant(self):
        """
        Test successful creation of a Tenant instance.
        Verifies that all required fields (id, name, domain, is_active) 
        are properly set and saved to the database.
        """
        tenant = TenantFactory()
        assert tenant.id is not None
        assert tenant.name is not None
        assert tenant.domain is not None
        assert tenant.is_active is True
    
    @pytest.mark.django_db
    def test_tenant_str(self):
        """
        Test the __str__ method of the Tenant model.
        Verifies that string representation returns the tenant's name,
        ensuring proper display in admin panel and debugging.
        """
        tenant = TenantFactory(name="Test Tenant")
        assert str(tenant) == "Test Tenant"
    
    @pytest.mark.django_db
    def test_unique_domain(self):
        """
        Test the unique constraint on the domain field.
        Verifies that creating two tenants with the same domain raises an exception,
        ensuring data integrity at the database level.
        """
        TenantFactory(domain="test")
        with pytest.raises(Exception):  # IntegrityError یا ValidationError
            TenantFactory(domain="test")