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


class EventRegistrationForm(forms.Form):
    membership_choices = [("isMember", "Oui"), ("isNotMember", "Non")]
    plan_choices = [
        ("reduced", "Réduit - CHF/EUR 10 par année (CHF/EUR 15 pour les non-membres)"),
        ("normal", "Normal - CHF/EUR 20 par année (CHF/EUR 25 pour les non-membres)"),
        ("support", "Soutien - CHF/EUR 25 par année (CHF/EUR 30 pour les non-membres)"),
    ]
    membership = forms.ChoiceField(
        choices=membership_choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    plan = forms.ChoiceField(
        choices=plan_choices,
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
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control normal-input", "placeholder": "Email"}
        ),
        required=True,
    )
    phone = forms.CharField(
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Téléphone"}
        ),
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
    # Hidden input to store the event date
    event = forms.DateField(
        widget=forms.HiddenInput(),
        required=False,
    )
    