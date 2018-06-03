from django.contrib import admin
from .models import PeerReview


class PeerReviewAdmin(admin.ModelAdmin):
    list_display = ('session',
                    'student',
                    'reviewed_by',
                    'feedback',
                    'score')
    search_fields = ['session',
                     'student',
                     'reviewed_by',
                     'score']
    list_filter = ['session',
                   'student',
                   'reviewed_by',
                   'score']


admin.site.register(PeerReview, PeerReviewAdmin)
