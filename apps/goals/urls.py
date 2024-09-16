"""goals url project file
"""

from django.urls import path

from . import views

app_name = "goals"

urlpatterns = [
    path("goals", views.goal_create, name="create"),
    path("goal-completions", views.create_goal_completion, name="create-goal-completion"),
    path("pending-goals", views.get_pending_goals, name="get-pending"),
    path("summary", views.get_summary, name="summary"),
]
