"""main goals url endpoints
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Goal, GoalsCompletions
from .serializers import GoalSerializer


@api_view(["POST"])
def goal_create(request):
    """create a new goal"""
    serializer = GoalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def complete_goal(request):
    Response({"status": "success"})


def get_pending_goals(request):
    Response({"status": "success"})


def get_summary(request):
    Response({"status": "success"})
