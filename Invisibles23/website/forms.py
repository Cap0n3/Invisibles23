from django import forms
from .validators import validate_names, validate_address, validate_zipcode


class MembershipForm(forms.Form):
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

