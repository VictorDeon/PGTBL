from django.conf.urls import url, include
from . import views

app_name = 'peer_review'

review_patterns = [
    url(
        r'^review/$',
        views.PeerReviewView.as_view(),
        name='review'
    ),
]

urlpatterns = [
    # /profile/<discipline.slug>/sessions/<session.id>/
    url(
        r'^profile/(?P<slug>[\w_-]+)/sessions/(?P<pk>[0-9]+)/',
        include(review_patterns)
    ),
]
