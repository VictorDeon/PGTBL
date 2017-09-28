from django.contrib import admin
from .models import Tag, News


class NewsAdmin(admin.ModelAdmin):
    """
    News admin news form configuration.
    """

    list_display = ['title', 'created_at']
    search_display = ['title']
    list_filter = ['created_at']


admin.site.register(News, NewsAdmin)
admin.site.register(Tag)
