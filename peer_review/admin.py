from django.contrib import admin
from .models import PeerReview


class PeerReviewAdmin(admin.ModelAdmin):
    list_display = ('username_received',
                    'username_gave',
                    'feedback',
                    'score')
    search_fields = ['username_received',
                     'username_gave',
                     'score']
    list_filter = ['username_received',
                   'username_gave',
                   'score']


admin.site.register(PeerReview, PeerReviewAdmin)
