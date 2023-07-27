from django.core.exceptions import ValidationError
import re


def validate_names(value):
    match = re.findall(r"[#!?*%&:;,_<>+=$£\[\]()\d]", value)

    if value.isdigit():
        raise ValidationError("Le nom ne peut pas être un nombre")
    elif len(value) < 2 or len(value) > 50:
        raise ValidationError("Le nom doit contenir entre 2 et 50 caractères")
    elif match:
        # Get the special characters in the string
        special_characters = [char for char in match if len(match) > 0]
        raise ValidationError(
            "Le nom ne peut pas contenir les caractères suivants : {}".format(
                ", ".join(special_characters)
            )
        )


def validate_address(value):
    match = re.findall(r"[#!?*%&:;_<>+=$£\[\]]", value)

    if value.isdigit():
        raise ValidationError("L'adresse ne peut pas être juste un nombre")
    elif len(value) < 5 and len(value) > 100:
        raise ValidationError("L'adresse doit contenir entre 5 et 50 caractères")
    elif match:
        # Get the special characters in the string
        special_characters = [char for char in match if len(match) > 0]
        raise ValidationError(
            "L'adresse ne peut pas contenir les caractères suivants : {}".format(
                ", ".join(special_characters)
            )
        )
