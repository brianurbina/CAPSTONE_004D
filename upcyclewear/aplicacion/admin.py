from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    # Los campos que se mostrarán en el formulario de administración
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'direccion', 'fotoperfil')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('user_type', 'rut', 'logotipo')}),
    )
    # Los campos que se mostrarán en la lista de usuarios
    list_display = ('username', 'email', 'user_type', 'telefono', 'direccion')
    # Los campos que se podrán buscar en la lista de usuarios
    search_fields = ('username', 'email', 'user_type')
    # Los campos por los que se puede ordenar la lista de usuarios
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
# Puedes optar por desregistrar el grupo si no lo necesitas
admin.site.unregister(Group)
