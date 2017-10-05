from django.contrib import admin
from .models import Tag, News


class NewsAdmin(admin.ModelAdmin):
    """
    Admin news form configuration.
    """

    list_display = ['title', 'created_at']
    search_display = ['title']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    """
    Admin tag form configuration.
    """

    list_display = ['title']
    search_display = ['title']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)
