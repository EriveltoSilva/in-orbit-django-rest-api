"""utils functions form goals app"""

from django.utils.timezone import now, timedelta


def get_first_and_last_day_of_the_week():
    """
    Get the first and last day of the week.
    """
    # Pegar o dia de hoje
    today = now().date()

    # Calcular o primeiro e o último dia da semana
    first_day_of_week = today - timedelta(days=today.weekday())
    last_day_of_week = first_day_of_week + timedelta(days=6)

    return first_day_of_week, last_day_of_week
