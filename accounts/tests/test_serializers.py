import pytest
from accounts.serializers import RegisterSerializer
from users.tests.factories import UserFactory
from core.tests.factories import TenantFactory

class TestRegisterSerializer:
    """
    Unit tests for RegisterSerializer.
    Tests cover user registration, password hashing, and validation.
    """
    
    @pytest.mark.django_db
    def test_register_user(self):
        """
        Test user registration through serializer.
        Verifies that password is hashed and user is created correctly.
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'testpass123'
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@test.com'
        assert user.check_password('testpass123')  # Password should be hashed
        assert user.password != 'testpass123'  # Should not be plain text
    
    @pytest.mark.django_db
    def test_register_validation_required_fields(self):
        """
        Test serializer validation for required fields.
        Verifies that missing required fields raise validation errors.
        """
        data = {
            'email': 'test@test.com'
            # Missing username and password
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
    
    @pytest.mark.django_db
    def test_register_password_write_only(self):
        """
        Test that password field is write-only.
        Verifies that password is not included in serialized output.
        """
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpass123'
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        # Serialize the created user
        output_serializer = RegisterSerializer(user)
        assert 'password' not in output_serializer.data  # Should not be in output

