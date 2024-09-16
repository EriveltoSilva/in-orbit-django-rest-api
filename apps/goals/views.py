"""main goals url endpoints
"""

from rest_framework.response import Response


# Create your views here.
def create_goal(request):
    Response({"status": "success"})


def complete_goal(request):
    Response({"status": "success"})


def get_pending_goals(request):
    Response({"status": "success"})


def get_summary(request):
    Response({"status": "success"})
