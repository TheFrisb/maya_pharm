# myapp/templatetags/custom_filters.py
from datetime import datetime

import pytz
from django import template

register = template.Library()


@register.simple_tag
def check_open_status():
    # Skopje timezone
    skopje_tz = pytz.timezone("Europe/Skopje")
    current_time = datetime.now(skopje_tz).time()

    # Define the opening and closing times
    opening_time = datetime.strptime("08:00", "%H:%M").time()
    closing_time = datetime.strptime("21:00", "%H:%M").time()

    if opening_time <= current_time <= closing_time:
        return "<span>Отворено во моментот (08:00 - 21:00)</span>"

    return '<span style="color:red">Затворено во моментот (08:00 - 21:00)</span>'
