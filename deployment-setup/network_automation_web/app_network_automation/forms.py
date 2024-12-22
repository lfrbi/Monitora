# forms.py
from django import forms
from .models import Device

class VendorSelectionForm(forms.Form):
    VENDOR_CHOICES = Device.VENDOR_CHOICES

    vendor = forms.ChoiceField(choices=VENDOR_CHOICES)