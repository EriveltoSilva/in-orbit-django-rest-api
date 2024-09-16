"""main goals url endpoints
"""

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils.timezone import now, timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import utils
from .models import Goal, GoalsCompletions
from .serializers import GoalsCompletionsSerializer, GoalSerializer


@api_view(["POST"])
def goal_create(request):
    """Create a new goal.

    This view handles POST requests to create a new goal. It expects the request data to
    be formatted according to the GoalSerializer. If the data is valid, the goal is saved
    and a 201 Created response is returned with the serialized goal data. If the data is
    invalid, a 400 Bad Request response is returned with the validation errors.

    Parameters:
    - request (HttpRequest): The HTTP request object containing the data for the new goal.

    Returns:
    - Response: The HTTP response object with a status code indicating the result of the
      create operation, and the serialized data or errors as appropriate.
    """
    serializer = GoalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_goal_completion(request) -> Response:
    """Create a goal completion for the current week.

    This function checks if the goal has been completed the desired number of times
    within the current week. If not, it allows the creation of a new goal completion.

    Args:
        request: The HTTP request object containing the 'goalId'.

    Returns:
        Response: A JSON response with the created goal completion data, or an error message if the goal
        has already been completed for the week or if the goal is not found.
    """
    goal_id = request.data.get("goalId")
    try:
        goal = Goal.objects.get(id=goal_id)
    except Goal.DoesNotExist:
        return Response({"error": "Goal not found."}, status=status.HTTP_404_NOT_FOUND)

    # Define the first and last day of the current week
    today = now().date()
    first_day_of_week = today - timedelta(days=today.weekday())  # Starts on Monday
    last_day_of_week = first_day_of_week + timedelta(days=6)  # Ends on Sunday

    # Count the goal completions for the current week
    completions_count = GoalsCompletions.objects.filter(
        goal=goal, created_at__date__gte=first_day_of_week, created_at__date__lte=last_day_of_week
    ).count()

    if completions_count >= goal.desired_weekly_frequency:
        return Response({"error": "Goal already completed this week!"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new goal completion
    goal_completion = GoalsCompletions.objects.create(goal=goal)

    serializer = GoalsCompletionsSerializer(goal_completion)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_pending_goals(request) -> Response:
    """Retrieve the list of goals pending completion for the current week.

    This function calculates the number of times each goal was completed during the
    current week and compares it with the desired weekly frequency. It returns a list
    of goals with their completion status for the week.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A JSON response containing the list of goals with their
        ID, title, desired weekly frequency, and number of completions for the current week.
    """

    # Get the first and last day of the current week
    first_day_of_week, last_day_of_week = utils.get_first_and_last_day_of_the_week()

    # Filter goals created up to the end of the week
    goals_created_up_to_week = Goal.objects.filter(created_at__lte=last_day_of_week)

    # Count the goals completed during the week
    goal_completion_counts = (
        GoalsCompletions.objects.filter(created_at__gte=first_day_of_week, created_at__lte=last_day_of_week)
        .values("goal")
        .annotate(completionsCount=Count("id"))
    )

    # Create a dictionary of completions for easy access
    completions_dict = {item["goal"]: item["completionsCount"] for item in goal_completion_counts}

    # Add the completions count for each goal
    pending_goals = []
    for goal in goals_created_up_to_week:
        completions_count = completions_dict.get(goal.id, 0)
        pending_goals.append(
            {
                "id": goal.id,
                "title": goal.title,
                "desired_weekly_frequency": goal.desired_weekly_frequency,
                "completionsCount": completions_count,
            }
        )

    # Return the pending goals of the week
    serializer = GoalSerializer(pending_goals, many=True)
    return Response({"pending_goals": serializer.data})


@api_view(["GET"])
def get_summary(request) -> Response:
    """Retrieve a summary of goals and their completions for the current week.

    This function calculates the total number of completed goals and compares it
    with the desired weekly frequency of all goals. It returns a summary of completed
    goals per day and the total number of completions for the week.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A JSON response containing the total completions, the desired weekly frequency,
        and the number of goals completed per day.
    """

    # Get the first and last day of the current week
    first_day_of_week, last_day_of_week = utils.get_first_and_last_day_of_the_week()

    # Filter goals created up to the last day of the week
    goals_created_up_to_week = Goal.objects.filter(created_at__lte=last_day_of_week)

    # Filter goals completed during the week
    goals_completed_in_week = GoalsCompletions.objects.filter(
        created_at__gte=first_day_of_week, created_at__lte=last_day_of_week
    ).annotate(
        completed_at_date=TruncDate("created_at")  # Group by date
    )

    # Count the total number of goals completed during the week
    completed_count = goals_completed_in_week.count()

    # Sum the desired weekly frequency of the goals created
    total_desired_weekly_frequency = (
        goals_created_up_to_week.aggregate(total_frequency=Sum("desired_weekly_frequency"))["total_frequency"] or 0
    )

    # Create a dictionary to group completed goals by the day of the week
    goals_per_day = {}
    for completion in goals_completed_in_week:
        # Convert the datetime.date object to a string
        completion_date_str = completion.completed_at_date.strftime("%Y-%m-%d")
        goal_info = {
            "id": str(completion.goal.id),
            "title": completion.goal.title,
            "created_at": completion.goal.created_at,
        }

        if completion_date_str not in goals_per_day:
            goals_per_day[completion_date_str] = {"completions": 0, "goals_info": []}

        goals_per_day[completion_date_str]["completions"] += 1
        goals_per_day[completion_date_str]["goals_info"].append(goal_info)

    # Build the final response
    summary = {
        "completed": completed_count,
        "total": total_desired_weekly_frequency,
        "goals_per_day": goals_per_day,
    }

    return Response({"summary": summary})
