import pytest
from django.test import RequestFactory
from core.middleware import TenantMiddleware, get_current_tenant
from core.tests.factories import TenantFactory

class TestTenantMiddleware:
    """
    Unit tests for TenantMiddleware.
    Tests cover tenant identification from HTTP headers (X-Tenant-ID, X-Tenant-Domain)
    and behavior when no tenant header is provided.
    """
    
    @pytest.fixture
    def middleware(self):
        """Fixture providing TenantMiddleware instance for tests."""
        return TenantMiddleware(lambda request: None)
    
    @pytest.fixture
    def factory(self):
        """Fixture providing RequestFactory for creating test requests."""
        return RequestFactory()
    
    @pytest.mark.django_db
    def test_tenant_from_header_id(self, middleware, factory):
        """
        Test tenant identification from X-Tenant-ID HTTP header.
        Verifies that middleware correctly extracts tenant ID from request headers
        and sets both request.tenant and get_current_tenant() to the correct tenant instance.
        """
        tenant = TenantFactory()
        request = factory.get('/')
        request.META['HTTP_X_TENANT_ID'] = str(tenant.id)
        
        middleware.process_request(request)
        
        assert request.tenant == tenant
        assert get_current_tenant() == tenant
    
    @pytest.mark.django_db
    def test_tenant_from_header_domain(self, middleware, factory):
        """
        Test tenant identification from X-Tenant-Domain HTTP header.
        Verifies that middleware correctly identifies tenant by domain name
        when domain is provided in request headers.
        """
        tenant = TenantFactory(domain="test")
        request = factory.get('/')
        request.META['HTTP_X_TENANT_DOMAIN'] = "test"
        
        middleware.process_request(request)
        
        assert request.tenant == tenant
    
    def test_no_tenant_header(self, middleware, factory):
        """
        Test middleware behavior when no tenant header is provided.
        Verifies that request.tenant and get_current_tenant() return None,
        ensuring graceful handling of requests without tenant identification.
        """
        request = factory.get('/')
        middleware.process_request(request)
        
        assert request.tenant is None
        assert get_current_tenant() is None