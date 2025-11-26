import pytest
from audio.models import Reciter
from audio.tests.factories import ReciterFactory
from core.tests.factories import TenantFactory

class TestReciterModel:
    """
    Unit tests for Reciter model.
    Tests cover model creation, relationships, unique constraints, and string representation.
    """
    
    @pytest.mark.django_db
    def test_create_reciter(self):
        """
        Test successful creation of a Reciter instance.
        Verifies that all required fields (id, name, language, tenant) 
        are properly set and saved to the database.
        """
        reciter = ReciterFactory()
        assert reciter.id is not None
        assert reciter.name is not None
        assert reciter.language == "ar"
        assert reciter.tenant is not None


    @pytest.mark.django_db
    def test_reciter_belongs_to_tenant(self):
        """
        Test that reciter is correctly associated with a tenant.
        Verifies the ForeignKey relationship between Reciter and Tenant.
        """ 
        tenant = TenantFactory(domain="test")
        reciter = ReciterFactory(tenant=tenant)
        assert reciter.tenant == tenant
        assert reciter.tenant.domain == "test"

    @pytest.mark.django_db
    def test_reciter_str(self):
        """
        Test the __str__ method of the Reciter model.
        Verifies that string representation returns the reciter's name.
        """
        reciter = ReciterFactory(name = "Test Reciter")
        assert str(reciter) == "Test Reciter"

    @pytest.mark.django_db
    def test_unique_name_per_tenant(self):
        """
        Test unique constraint: same name can exist in different tenants.
        Verifies that two reciters with the same name can exist 
        if they belong to different tenants.
        """
        tenant1 = TenantFactory(domain="tenant1")
        tenant2 = TenantFactory(domain="tenant2")
        
        reciter1 = ReciterFactory(tenant=tenant1, name="Same Name")
        reciter2 = ReciterFactory(tenant=tenant2, name="Same Name")
        
        assert reciter1.name == reciter2.name
        assert reciter1.tenant != reciter2.tenant
    
    @pytest.mark.django_db
    def test_unique_name_same_tenant_fails(self):
        """
        Test that creating two reciters with the same name in the same tenant raises an exception.
        Verifies the unique_together constraint ('tenant', 'name').
        """
        tenant = TenantFactory()
        ReciterFactory(tenant=tenant, name="Unique Name")
        
        with pytest.raises(Exception):
            ReciterFactory(tenant=tenant, name="Unique Name")