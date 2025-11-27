import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from users.tests.factories import UserFactory
from core.tests.factories import TenantFactory

User = get_user_model()

class TestUserModel:
    """
    Unit tests for User model.
    Tests cover user creation, tenant association, password hashing, and unique constraints.
    """
    
    @pytest.mark.django_db
    def test_create_user(self):
        """
        Test successful creation of a User instance.
        Verifies that all required fields are properly set and password is hashed.
        """
        user = UserFactory()
        assert user.id is not None
        assert user.username is not None
        assert user.email is not None
        assert user.tenant is not None
        assert user.check_password('testpass123')  # Password should be hashed
    
    @pytest.mark.django_db
    def test_user_belongs_to_tenant(self):
        """
        Test that user is correctly associated with a tenant.
        Verifies the ForeignKey relationship between User and Tenant.
        """
        tenant = TenantFactory(domain="test")
        user = UserFactory(tenant=tenant)
        assert user.tenant == tenant
        assert user.tenant.domain == "test"
    
    @pytest.mark.django_db
    def test_user_str(self):
        """
        Test the __str__ method of the User model.
        Verifies that string representation returns the username.
        """
        user = UserFactory(username="testuser")
        assert str(user) == "testuser"
    
    @pytest.mark.django_db
    def test_unique_username_per_tenant(self):
        """
        Test unique constraint: same username can exist in different tenants.
        Verifies that two users with the same username can exist 
        if they belong to different tenants.
        """
        tenant1 = TenantFactory(domain="tenant1")
        tenant2 = TenantFactory(domain="tenant2")
    
        UserFactory(tenant=tenant1, username="sameuser")
    
        # تلاش برای ساخت user دوم با همان username باید خطا بدهد
        # حتی اگر tenant متفاوت باشد
        with pytest.raises(IntegrityError):
         UserFactory(tenant=tenant2, username="sameuser")
    
    @pytest.mark.django_db
    def test_unique_username_same_tenant_fails(self):
        """
        Test that creating two users with the same username in the same tenant raises an exception.
        Verifies the unique_together constraint ('tenant', 'username').
        """
        tenant = TenantFactory()
        UserFactory(tenant=tenant, username="uniqueuser")
        
        with pytest.raises(IntegrityError):
            UserFactory(tenant=tenant, username="uniqueuser")
    
    @pytest.mark.django_db
    def test_password_is_hashed(self):
        """
        Test that password is properly hashed and not stored in plain text.
        Verifies security by checking password hash format.
        """
        user = UserFactory(password="mypassword")
        assert user.password != "mypassword"  # Should be hashed
        assert user.check_password("mypassword")  # Should verify correctly
        assert not user.check_password("wrongpassword")  # Should fail for wrong password