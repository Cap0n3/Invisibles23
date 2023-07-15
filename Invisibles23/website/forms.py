from django import forms

# Create your forms here.
class MembershipForm(forms.Form):
    fname = forms.CharField(max_length=100, label='First Name')
    lname = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(max_length=100, label='Email')
    