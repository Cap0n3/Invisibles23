from django import forms
from .validators import validate_names, validate_address


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
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Prénom"}
        ),
        validators=[validate_names],
    )
    lname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Nom"}
        ),
        validators=[validate_names],
    )
    birthday = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control normal-input"}
        ),
    )
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Adresse"}
        ),
        validators=[validate_address],
    )
    zip_code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control normal-input", "placeholder": "Code postal"}
        ),
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control normal-input", "placeholder": "Ville"}
        ),
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control normal-input", "placeholder": "Email"}
        ),
    )

    # def clean_fname(self):
    #     fname = self.cleaned_data.get('fname')
    #     if not fname:
    #         raise forms.ValidationError("Veuillez entrer votre prénom.")
    #     elif len(fname) > 3:
    #         raise forms.ValidationError("Votre prénom est trop long.")
    #     return fname
