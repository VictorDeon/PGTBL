from django.contrib import admin
from .models import PeerReview


class PeerReviewAdmin(admin.ModelAdmin):
    list_display = ('session',
                    'username_received',
                    'username_gave',
                    'feedback',
                    'score')
    search_fields = ['session',
                     'username_received',
                     'username_gave',
                     'score']
    list_filter = ['session',
                   'username_received',
                   'username_gave',
                   'score']


admin.site.register(PeerReview, PeerReviewAdmin)
