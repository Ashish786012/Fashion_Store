from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        errors = []
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = cleaned_data.get('phone_number')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        
        if not email:
            errors.append(forms.ValidationError("Email is required!"))
        elif len(email) < 5:
            errors.append(forms.ValidationError("Email must be more than 5 characters long."))

        if len(first_name) < 2:
            errors.append(forms.ValidationError("First name must be at least 2 characters long."))

        if len(last_name) < 2:
            errors.append(forms.ValidationError("Last name must be at least 2 characters long."))

        

        if len(phone_number) != 10 or not phone_number.isdigit():
            errors.append(forms.ValidationError("Phone number must be exactly 10 digits."))

        if not password:
            errors.append(forms.ValidationError("Password is required!"))
        elif len(password) < 6:
            errors.append(forms.ValidationError("Password must be at least 6 characters long."))
        elif not confirm_password:
            errors.append(forms.ValidationError("Password confirmation is required."))
        elif password != confirm_password:
            errors.append(forms.ValidationError("Passwords do not match."))

        if errors:
            raise forms.ValidationError(errors)

        # You can add similar checks for other fields.

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
