from django import forms
from .validators import (
    validate_names,
    validate_address,
    validate_zipcode,
    validate_phone,
)
import re

class PhoneWidget(forms.TextInput):
    input_type = 'tel'

# Custom phone number field
class PhoneNumber(forms.Field):
    def __init__(
        self,
        required=True,
        label=None,
        initial=None,
        widget=None,
        help_text=None,
        validators=[],
        *args,
        **kwargs
    ):
        super().__init__(
            required=required,
            label=label,
            initial=initial,
            widget=widget or PhoneWidget(attrs={'placeholder': 'xxx-xxx-xxxx'}),
            help_text=help_text,
            validators=validators,
            *args,
            **kwargs
        )
    
    def clean(self, value):
        value = super().clean(value)
        if value is None:
            return value
        return value


class MembershipForm(forms.Form):
    """
    This form is used to register for a membership.
    """

    subscription_choices = [
        ("support", "Soutien - CHF/EUR 84 par année (CHF/EUR 7.70 par mois)"),
        ("normal", "Normal - CHF/EUR 50 par année (CHF/EUR 4.50 par mois)"),
        ("reduced", "Réduit - CHF/EUR 25 par année (CHF/EUR 2.50 par mois)"),
    ]
    frequency_choices = [
        ("yearly", "Annuellement"),
        ("monthly", "Mensuellement"),
    ]
    subscription = forms.ChoiceField(
        choices=subscription_choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    frequency = forms.ChoiceField(
        choices=frequency_choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    fname = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Prénom"}
        ),
        validators=[validate_names],
        required=True,
    )
    lname = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Nom"}
        ),
        validators=[validate_names],
        required=True,
    )
    birthday = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control normal-input"}
        ),
        required=False,
    )
    address = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Adresse"}
        ),
        validators=[validate_address],
        required=True,
    )
    zip_code = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Code postal"}
        ),
        validators=[validate_zipcode],
        required=True,
    )
    city = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Ville"}
        ),
        validators=[validate_names],
        required=True,
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control normal-input", "placeholder": "Email"}
        ),
        required=True,
    )


class EventRegistrationForm(forms.Form):
    """
    This form is used to register for an event (talk group).
    """

    membership_choices = [("isMember", "Oui"), ("isNotMember", "Non")]
    plan_choices = [
        ("reduced", "Réduit - CHF/EUR (CHF/EUR 15 pour les non-membres)"),
        ("normal", "Normal - CHF/EUR (CHF/EUR 25 pour les non-membres)"),
        ("support", "Soutien - CHF/EUR (CHF/EUR 30 pour les non-membres)"),
    ]
    membership_status = forms.ChoiceField(
        choices=membership_choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        # Define the initial value of the radio button
        # initial="isNotMember",
        required=True,
    )
    plan = forms.ChoiceField(
        choices=plan_choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial="normal",
        required=True,
    )
    fname = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Prénom"}
        ),
        validators=[validate_names],
        required=True,
    )
    lname = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Nom"}
        ),
        validators=[validate_names],
        required=True,
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control normal-input", "placeholder": "Email"}
        ),
        required=True,
    )
    phone = PhoneNumber(
        widget=PhoneWidget(
            attrs={"class": "form-control normal-input", "placeholder": "Téléphone"}
        ),
        validators=[validate_phone],
        required=True,
    )
    address = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Adresse"}
        ),
        validators=[validate_address],
        required=True,
    )
    zip_code = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Code postal"}
        ),
        validators=[validate_zipcode],
        required=True,
    )
    city = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Ville"}
        ),
        validators=[validate_names],
        required=True,
    )
    # Hidden input to store the event pk (NO NEED FOR THIS, CAN BE DONE WITH URL PARAMETER)
    # event = forms.IntegerField(widget=forms.HiddenInput(), required=True)
