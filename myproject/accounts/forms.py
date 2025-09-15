from django import forms

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class SignupForm(forms.Form):
    name = forms.CharField(max_length=150, label="Full name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label="Password")
    phone = forms.CharField(max_length=30, required=False, label="Phone (E.164 e.g. +92300...)")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False, label="Address")
