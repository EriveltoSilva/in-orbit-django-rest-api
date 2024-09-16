import uuid

from django.db import models


# Create your models here.
class Goal(models.Model):
    """goal model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    desired_weekly_frequency = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """goal model information"""

        verbose_name = "Meta"
        verbose_name_plural = "Metas"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """string representation of goal"""
        return str(self.title)


class GoalsCompletions(models.Model):
    """goals completions model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """goals-completions models information"""

        verbose_name = "Finalização de Meta"
        verbose_name_plural = "Finalizações de Metas"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """string representation of goal"""
        return f"Completions for:{self.goal}"
