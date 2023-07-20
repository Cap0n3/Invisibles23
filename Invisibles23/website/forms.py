from django import forms

# class DateInput(forms.DateInput):
#     input_type = 'date'

# Create your forms here.
class MembershipForm(forms.Form):
    discount = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
        required=False, 
        label="Contribution annuelle réduite à CHF 45 pour les bénéficiaires de l'AVS/AI, les stagiaires/étudiants, les personnes en difficulté financière.",
    )
    fname = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Prénom'}),
    )
    lname = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Nom'}),
    )
    birthday = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control normal-input'})
    )
    address = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Adresse'}),
    )
    zip_code = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Code postal'}),
    )
    city = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Ville'}),    
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control normal-input', 'placeholder': 'Email'}),
    )    