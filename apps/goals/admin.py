""" goals django admin classes"""

from django.contrib import admin

from .models import Goal, GoalsCompletions


# Register your models here.
class GoalAdmin(admin.ModelAdmin):
    """goal django admin"""

    list_display = ("id", "title", "desired_weekly_frequency", "created_at", "updated_at")
    list_display_links = ("id", "title", "desired_weekly_frequency", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("created_at",)
    list_per_page = 25


class GoalsCompletionsAdmin(admin.ModelAdmin):
    """goal-completions django admin"""

    list_display = ("id", "goal", "created_at", "updated_at")
    list_display_links = ("id", "goal", "created_at", "updated_at")
    list_per_page = 25


admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalsCompletions, GoalsCompletionsAdmin)
