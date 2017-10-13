from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import User
from .forms import UserCreationForm, UserForm


class UserAdmin(BaseUserAdmin):
    """
    New admin user form configuration.
    """
    # object edit form from user
    form = UserForm
    # How the admin form will be structured (Legenda, {atributos})
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email'
            )
        }),
        (_('Personal Information'), {
            'fields': (
                'name',
                'photo',
                'institution',
                'course',
                'is_teacher',
                'last_login',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        })
    )

    # class that represent the admin form only when adding a new user
    add_form = UserCreationForm
    # How the admin form will be structured only when adding a new user
    add_fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'is_teacher',
                'password1',
                'password2'
            )
        }),
    )

    # Fields that will be whown in django admin
    list_display = ['username',
                    'name',
                    'email',
                    'is_teacher',
                    'is_active',
                    'is_staff',
                    'created_at'
                    ]

    # Fields that will be search in django admin
    search_display = ['username',
                      'name',
                      'email'
                      ]

    # Fields that will be filtered in django admin
    list_filter = ['created_at',
                   'is_teacher',
                   'is_staff',
                   'institution'
                   ]


# Create models on django admin
admin.site.register(User, UserAdmin)
