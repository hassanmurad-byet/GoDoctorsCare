from django import template

register = template.Library()

@register.filter
def calculate_payment(duration_minutes):
    try:
        return int(duration_minutes) // 15 * 1000
    except (ValueError, TypeError):
        return 0