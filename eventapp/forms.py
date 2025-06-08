from django import forms
from eventapp.models import Booking

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

        widgets = {
            'cus_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'cus_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'name': forms.Select(attrs={'class': 'form-select'}),
            'booking_date': DateInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'cus_name': 'Customer Name',
            'cus_phone': 'Customer Phone',
            'name': 'Event Name',
            'booking_date': 'Booking Date:',
        }
