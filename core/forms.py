from django import forms
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

class DateForm(forms.Form):
   myDate = forms.DateField()

class GeeksForm(forms.Form):
    geeks_field = forms.DateField()

from django.shortcuts import render
from .forms import ServiceBusForm
from azure.servicebus import ServiceBusClient

from django import forms

class ServiceBusForm(forms.Form):
    conn_str = forms.CharField(
        label='Connection String',
        widget=forms.TextInput(attrs={'placeholder': 'Enter Connection String'})
    )

    def clean_conn_str(self):
        conn_str = self.cleaned_data['conn_str']
        try:
            ServiceBusClient.from_connection_string(conn_str)
        except Exception as e:
            raise forms.ValidationError("Invalid connection string")
        return conn_str