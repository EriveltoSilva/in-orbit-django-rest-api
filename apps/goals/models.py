import uuid

from django.db import models


# Create your models here.
class Goal(models.Model):
    """goal model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    desired_weeklyFrequency = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """meta models information"""

        verbose_name = "Goal"
        verbose_name_plural = "Goals"
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

    def __str__(self) -> str:
        """string representation of goal"""
        return f"Completions for:{self.goal}"
