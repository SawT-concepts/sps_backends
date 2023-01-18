from django import forms
from .models import *


class Payment_form(forms.ModelForm):
    
    class Meta:
        model = payment    
        fields = ("registration_number", "email",)

        labels = {
             "registration_number":"",
             "email":"",
         }

        widgets = {

            'registration_number': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Registration number'}),
            'email': forms.EmailInput(attrs={'class': 'w-input', 'placeholder': 'Email Address'}),
         }


class Amount_form (forms.ModelForm):

    class Meta:
        model = payment 
        fields = ("amount_paid",)

        labels = {
             "amount_paid": ""
        }

        widgets = {
            'amount_paid': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Enter the amount you want to pay'}),
        }