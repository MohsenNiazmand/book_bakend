# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Tenant Information', {'fields': ('tenant',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Tenant Information', {'fields': ('tenant',)}),
    )
    list_display = ('username', 'email', 'tenant', 'is_staff', 'is_active')
    list_filter = ('tenant', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')