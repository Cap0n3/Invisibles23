from django import forms

# Create your forms here.
class MembershipForm(forms.Form):
    fname = forms.CharField(max_length=100, label='First Name')
    lname = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(max_length=100, label='Email')
    discount = forms.BooleanField(widget=forms.CheckboxInput, required=False, label="Contribution annuelle réduite à CHF 45 pour les bénéficiaires de l'AVS/AI, les stagiaires/étudiants, les personnes en difficulté financière.")
    