from django import forms
from .models import Customer_Support, Vehicle


class customer_support_form(forms.ModelForm):
    class Meta:
        model = Customer_Support
        fields = ('Email', 'Comment')


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        # vehicle_id is auto-generated server-side, not user-entered
        fields = ('brand', 'color', 'model', 'year', 'license_plate')
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
        }