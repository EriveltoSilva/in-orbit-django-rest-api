"""main goals url endpoints
"""

from django.db.models import Count
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Goal, GoalsCompletions
from .serializers import GoalsCompletionsSerializer, GoalSerializer


@api_view(["POST"])
def goal_create(request):
    """create a new goal"""
    serializer = GoalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_goal_completion(request):
    """create a goal completion"""
    goal_id = request.data.get("goalId")
    try:
        goal = Goal.objects.get(id=goal_id)
    except Goal.DoesNotExist:
        return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)

    # Definir o primeiro e o último dia da semana
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Começa na segunda-feira
    end_of_week = start_of_week + timedelta(days=6)  # Termina no domingo

    # Contar as conclusões de metas para a semana atual
    completions_count = GoalsCompletions.objects.filter(
        goal=goal, created_at__date__gte=start_of_week, created_at__date__lte=end_of_week
    ).count()

    if completions_count >= goal.desired_weekly_frequency:
        return Response({"error": "Goal already completed this week!"}, status=status.HTTP_400_BAD_REQUEST)

    # Criar nova conclusão de meta
    goal_completion = GoalsCompletions.objects.create(goal=goal)

    serializer = GoalsCompletionsSerializer(goal_completion)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_pending_goals(request):
    Response({"status": "success"})


def get_summary(request):
    Response({"status": "success"})
