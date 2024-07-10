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
    match = re.search(r"^[0-9]{10}$", value)

    if not match:
        raise ValidationError("Le numéro de téléphone n'est pas valide.")
    elif len(value) < 10 or len(value) > 10:
        raise ValidationError("Le numéro de téléphone doit contenir 10 chiffres.")
    elif not value.isdigit():
        raise ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")