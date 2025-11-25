from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.middleware import get_current_tenant
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        tenant = get_current_tenant()
        serializer.save(tenant=tenant)
