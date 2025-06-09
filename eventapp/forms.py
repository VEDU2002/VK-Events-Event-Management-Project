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

class OTPRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email'
        })
    )

class OTPResetForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'readonly': 'readonly'  # Make it readonly since it comes from previous step
        })
    )
    otp = forms.CharField(
        label="OTP",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit OTP'
        })
    )
    new_password = forms.CharField(
        label="New Password",
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password (minimum 6 characters)'
        })
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if otp and not otp.isdigit():
            raise forms.ValidationError("OTP must contain only numbers.")
        return otp

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

class OTPVerifyForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    otp = forms.CharField(label="Enter the OTP")
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password")   
