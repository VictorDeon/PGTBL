from django.urls import path, include
from . import views

app_name = "peer_review"

peer_review_patterns = [
    path(
        '',
        views.PeerReviewView.as_view(),
        name='list'
    ),
    path(
        'update',
        views.PeerReviewUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:student_id>/answer/<int:peer_review_page>/',
        views.PeerReviewAnswerView.as_view(),
        name='answer-review'
    )
]

urlpatterns = [
    path('profile/<slug:slug>/sessions/<int:pk>/peer-review/', include(peer_review_patterns))
]
