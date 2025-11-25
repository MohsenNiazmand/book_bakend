from threading import local
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant

_thread_locals = local()

def get_current_tenant():
    """Get current tenant from thread local storage"""
    return getattr(_thread_locals, 'tenant', None)

def set_current_tenant(tenant):
    """Set current tenant in thread local storage"""
    _thread_locals.tenant = tenant

class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to identify tenant from:
    1. X-Tenant-ID header
    2. X-Tenant-Domain header  
    3. Subdomain (e.g., tenant1.example.com)
    4. Query parameter 'tenant' (for testing)
    """
    
    def process_request(self, request):
        tenant = None
        
        # Method 1: Check X-Tenant-ID header
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id:
            try:
                tenant = Tenant.objects.get(id=tenant_id, is_active=True)
            except Tenant.DoesNotExist:
                pass
        
        # Method 2: Check X-Tenant-Domain header
        if not tenant:
            tenant_domain = request.headers.get('X-Tenant-Domain')
            if tenant_domain:
                try:
                    tenant = Tenant.objects.get(domain=tenant_domain, is_active=True)
                except Tenant.DoesNotExist:
                    pass
        
        # Method 3: Check subdomain
        if not tenant:
            host = request.get_host().split(':')[0]  # Remove port if present
            parts = host.split('.')
            if len(parts) >= 2:
                subdomain = parts[0]
                try:
                    tenant = Tenant.objects.get(domain=subdomain, is_active=True)
                except Tenant.DoesNotExist:
                    pass
        
        # Method 4: Check query parameter (for testing)
        if not tenant:
            tenant_domain = request.GET.get('tenant')
            if tenant_domain:
                try:
                    tenant = Tenant.objects.get(domain=tenant_domain, is_active=True)
                except Tenant.DoesNotExist:
                    pass
        
        set_current_tenant(tenant)
        request.tenant = tenant
        
    def process_response(self, request, response):
        # Clean up thread local storage
        set_current_tenant(None)
        return response


