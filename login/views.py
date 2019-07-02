from django.shortcuts import render
from .forms import RegFrom, LoginFrom
from .models import User
import ctypes  # An included library with Python install.


def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def login_view(request):
    my_form = LoginFrom()
    if request.method == "POST":
        my_form = LoginFrom(request.POST)
        if my_form.is_valid():
            message_box('Welcome', 'Welcome to our site!!', 1)
            #my_form = LoginFrom()
            return render(request, 'home.html')
        else:
            print(my_form.errors)
    context = {
        'form': my_form,
    }
    return render(request, 'login.html', context)


def reg_view(request):
    my_form = RegFrom()
    if request.method == "POST":
        my_form = RegFrom(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data.get('confirm_password'))
            User.objects.create(
                user_name=my_form.cleaned_data.get("user_name"),
                password=my_form.cleaned_data.get("password"),
                phone_number=my_form.cleaned_data.get("phone_number"),
                email_id=my_form.cleaned_data.get("email_id"),
            )
            message_box('Congratilations', 'You have successfully registered and logged in!!STAY WITH US :)', 1)
            # my_form = LoginFrom()
            return render(request, 'home.html')
        else:
            print(my_form.errors)
    context = {
        'form': my_form,
        'message': "successfully registered!"
    }
    return render(request, 'reg.html', context)


