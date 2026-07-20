from django import template

register = template.Library()

@register.filter
def star_rating(value):
    """
    Raqamli reytingni (masalan 3.7) yulduzchalarga aylantiradi.
    .5 va undan yuqori bo'lsa -> yuqoriga yaxlitlanadi
    .5 dan kichik bo'lsa -> pastga yaxlitlanadi
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0

    whole = int(value)
    frac = value - whole

    rounded = whole + 1 if frac >= 0.5 else whole
    rounded = max(0, min(rounded, 5))  # 0-5 oralig'ida ushlab turish

    full_stars = "★" * rounded
    empty_stars = "☆" * (5 - rounded)

    return full_stars + empty_stars

@register.filter
def format_price(value):
    """
    Narxni minglik guruhlarga ajratadi: 1234567 -> "1 234 567"
    """
    try:
        value = int(round(float(value)))
    except (TypeError, ValueError):
        return value

    return "{:,}".format(value).replace(",", " ")