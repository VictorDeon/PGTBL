from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    New admin user form configuration.
    """

    list_display = ['name', 'email', 'institution', 'created_at']
    search_display = ['name', 'email']
    list_filter = ['created_at', 'is_teacher', 'is_staff', 'institution']


# Create models on django admin
admin.site.register(User, UserAdmin)
