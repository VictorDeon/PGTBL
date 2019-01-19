from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('disciplines.urls')),
    path('', include('groups.urls')),
    path('', include('files.urls')),
    path('', include('modules.urls')),
    path('', include('questions.urls')),
    path('', include('grades.urls')),
    path('', include('peer_review.urls')),
    path('', include('practical_test.urls')),
    path('', include('exercises.urls')),
    path('', include('irat.urls')),
    path('', include('grat.urls')),
    path('', include('rank.urls')),
    path('', include('dashboard.urls')),
    path('', include('appeals.urls')),
    path('', include('forum.urls')),
    path('', include('notification.urls'))
]

# While in development mode we will use relative URL for static and average
# files. In production mode we will no longer need this folder as we will store
# everything on a server
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
