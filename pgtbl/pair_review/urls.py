from django.urls import path, include
from . import views

app_name = "pair_review"

pair_review_patterns = [
    path(
        '',
        views.PairReviewView.as_view(),
        name='list'
    )
]

urlpatterns = [
    path('profile/<slug:slug>/sessions/<int:pk>/peer-review/', include(pair_review_patterns))
]
