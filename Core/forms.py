from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, RescueRequest, Booking, AdoptionRequest

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class RescueRequestForm(forms.ModelForm):
    class Meta:
        model = RescueRequest
        fields = ['name', 'phone_number', 'date', 'time', 'animal_type', 'description', 'location', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the situation...', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location', 'id': 'location-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pet_name', 'animal_type', 'booking_date']
        widgets = {
            'pet_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us why you want to adopt this pet...', 'rows': 4}),
        }
