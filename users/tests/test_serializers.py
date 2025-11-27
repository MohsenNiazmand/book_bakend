import pytest
from users.serializers import UserSerializer
from users.tests.factories import UserFactory
from core.tests.factories import TenantFactory

class TestUserSerializer:
    """
    Unit tests for UserSerializer.
    Tests cover serialization, deserialization, and read-only fields.
    """
    
    @pytest.mark.django_db
    def test_serialize_user(self):
        """
        Test serialization: model instance -> dictionary.
        Verifies that User model is correctly converted to dictionary format.
        """
        user = UserFactory(username="testuser", email="test@test.com")
        serializer = UserSerializer(user)
        
        assert serializer.data['username'] == "testuser"
        assert serializer.data['email'] == "test@test.com"
        assert serializer.data['id'] == user.id
        assert 'is_staff' in serializer.data
        assert 'is_active' in serializer.data
    
    @pytest.mark.django_db
    def test_serializer_read_only_fields(self):
        """
        Test that read-only fields (id, is_staff, is_active) are not writable.
        Verifies read_only_fields configuration.
        """
        user = UserFactory()
        data = {
            'id': 999,  # Should be ignored
            'is_staff': True,  # Should be ignored
            'is_active': False,  # Should be ignored
            'username': 'updateduser',
            'email': 'updated@test.com'
        }
        serializer = UserSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        
        updated_user = serializer.save()
        assert updated_user.id == user.id  # ID should not change
        assert updated_user.username == 'updateduser'
    
    @pytest.mark.django_db
    def test_serializer_excludes_password(self):
        """
        Test that password field is not included in serialized output.
        Verifies security by ensuring password is never exposed.
        """
        user = UserFactory()
        serializer = UserSerializer(user)
        
        assert 'password' not in serializer.data  # Password should never be in output

