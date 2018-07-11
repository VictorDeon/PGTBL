from django.contrib import admin
from .models import Tag, News


class NewsAdmin(admin.ModelAdmin):
    """
    Admin news form configuration.
    """

    # List title and created_at field in discipline list admin
    list_display = ['title', 'created_at']

    # Search for discipline title
    search_display = ['title']

    # Filter discipline by his creation date
    list_filter = ['created_at']

    # Pre populate slug field with title
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    """
    Admin tag form configuration.
    """

    # List title in tag list admin
    list_display = ['title']

    # Search for tag title
    search_display = ['title']

    # Pre populate slug field with title
    prepopulated_fields = {'slug': ('title',)}


# Register News and Tag inside admin
admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)
