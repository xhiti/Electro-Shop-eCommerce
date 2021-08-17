from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control ps-form__input'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control ps-form__input'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control ps-form__input'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control ps-form__input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control ps-form__input'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control ps-form__input'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirmed_password = cleaned_data.get('confirm_password')

        if password != confirmed_password:
            raise forms.ValidationError(
                "Password doesn't match!"
            )


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
        'class': 'form-control ps-input'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
        'class': 'form-control ps-input'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'form-control ps-input'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']


class UserProfileForm(forms.ModelForm):

    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 1',
        'class': 'form-control ps-input'
    }))

    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 2',
        'class': 'form-control ps-input'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'form-control ps-input'
    }))

    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'State',
        'class': 'form-control ps-input'
    }))

    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Country',
        'class': 'form-control ps-input'
    }))

    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
        'placeholder': 'Profile Picture',
        'class': 'form-control ps-input',
        'attrs': 'disabled'
    }))

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']

