from login.models import User
from django.forms import ModelForm


# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password')


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone_number'
        )
