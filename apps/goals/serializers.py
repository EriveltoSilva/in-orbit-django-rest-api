""" model serializers"""

from rest_framework import serializers

from .models import Goal, GoalsCompletions


class GoalSerializer(serializers.ModelSerializer):
    """goal serializer"""

    class Meta:
        """goal serializer meta"""

        model = Goal
        fields = [
            "id",
            "title",
            "desired_weekly_frequency",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
        extra_kwargs = {"title": {"required": True}, "desired_weekly_frequency": {"required": True}}
        ordering = ["-created_at"]


class GoalsCompletionsSerializer(serializers.ModelSerializer):
    """goal-completions serializer"""

    class Meta:
        """goal serializer meta"""

        model = GoalsCompletions
        fields = [
            "id",
            "goal",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
        ordering = ["-created_at"]
