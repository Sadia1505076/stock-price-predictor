from .models import User
from django import forms
from .validators import max_length_validator


class RegFrom(forms.Form):
    user_name = forms.CharField(validators=[
            max_length_validator(
                20, 'user name'
                )
            ])
    phone_number = forms.CharField(required=False, validators=[
            max_length_validator(
                25, 'phone no'
                )
            ])
    email_id = forms.EmailField(validators=[
            max_length_validator(
                50, 'email id'
                )
            ])
    password = forms.CharField(widget=forms.PasswordInput, validators=[
            max_length_validator(
                45, 'password'
                )
            ])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")
        if password1 != password2:
            raise forms.ValidationError("Passwords must be identical.")

        return cleaned_data

    def clean_phone_number(self):
        phone_no = self.cleaned_data.get("phone_number")
        if not phone_no.isdigit():
            raise forms.ValidationError("enter a valid phone number")
        else:
            return phone_no

    def clean_user_name(self):
        user_name = self.cleaned_data.get("user_name")
        try:
            user_from_db = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            user_from_db = None
        if user_from_db is not None:
            raise forms.ValidationError("sorry, user exists!")
        else:
            return user_name


class LoginFrom(forms.Form):
    user_name = forms.CharField(validators=[
            max_length_validator(
                20, 'user name'
                )
            ])

    password = forms.CharField(widget=forms.PasswordInput, validators=[
            max_length_validator(
                45, 'password'
                )
            ])

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        password = cleaned_data.get("password")
        user_name = cleaned_data.get("user_name")
        try:
            user_from_db = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            user_from_db = None
        if user_from_db is None:
            raise forms.ValidationError("user doesn't exist!")
        else:
            pass_from_db = User.objects.get(user_name=user_name).password
            if pass_from_db != password:
                raise forms.ValidationError("wrong password,try again!")
            else:
                return cleaned_data


