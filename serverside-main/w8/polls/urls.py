from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.PollView.as_view(), name="detail"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
]