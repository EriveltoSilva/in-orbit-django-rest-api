"""goals url project file
"""

from django.urls import path

from . import views

app_name = "goals"

urlpatterns = [
    path("/goals", views.create_goal, name="create"),
    path("/goal-completions", views.complete_goal, name="completions"),
    path("/pending-goals", views.get_pending_goals, name="get-pending"),
    path("/summary", views.get_summary, name="summary"),
]
