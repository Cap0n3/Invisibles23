from django import forms

# Create your forms here.
class MembershipForm(forms.Form):
    # create lookup_key hidden field with name "lookup_key" and value "membership-test"
    fname = forms.CharField(max_length=100, label='First Name')
    lname = forms.CharField(max_length=100, label='Last Name')
    