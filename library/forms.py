from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rental

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['book_code', 'book_description', 'rental_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the authenticated user from the view
        super(RentalForm, self).__init__(*args, **kwargs)
        self.fields['book_code'].widget = forms.HiddenInput()  # Hide the book_code field
        self.fields['book_description'].widget.attrs['readonly'] = True  # Make book_description field readonly
        self.instance.student = user  # Assign the authenticated user to the student field
