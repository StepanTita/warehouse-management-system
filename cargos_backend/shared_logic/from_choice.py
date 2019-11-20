from django.core.exceptions import ValidationError


def to_category_name(choice_key, choices):
    for choice in choices:
        key, value = choice
        if key == choice_key:
            return value
    raise ValidationError


def to_format(field):
    from .choices import FIELDS_CHOICES
    return f"{to_category_name(int(field), FIELDS_CHOICES).lower().replace(' ', '_')}"


def to_view_choice(x):
    return x[0], str(x[1]).rpartition('.')[2].replace('_', ' ').capitalize()
