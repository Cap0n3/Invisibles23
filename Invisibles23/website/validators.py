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
    elif len(value) < 5 or len(value) > 100:
        raise ValidationError("L'adresse doit contenir entre 5 et 100 caractères")
    elif match:
        # Get the special characters in the string
        special_characters = [char for char in match if len(match) > 0]
        raise ValidationError(
            "L'adresse ne peut pas contenir les caractères suivants : {}".format(
                ", ".join(special_characters)
            )
        )


def validate_zipcode(value):
    match = re.search("^[a-zA-Z0-9]{2,}\s?-?[a-zA-Z0-9]{0,}$", value)

    if not match:
        raise ValidationError("Le code postal n'est pas valide.")
    elif len(value) < 2 or len(value) > 50:
        raise ValidationError("Le code postal doit contenir entre 2 et 50 caractères")


# TO TEST
def validate_phone(value):
    match = re.search(r"^(\+(41|33)|00\s?(41|33)|0\d{1,2})(\s?\(0\))?(\s)?(\d{1,2})(\s)?(\d{2,3})(\s)?(\d{2})(\s)?(\d{2})(\s)?(\d{2})?$", value)

    if not match:
        raise ValidationError("Le numéro de téléphone non valide (ex: +41 79 123 45 67, 0033 6 12 34 56 78, 079 123 45 67).")
    elif len(value) > 80:
        raise ValidationError("Le numéro de téléphone est trop long.")
