import ctypes
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import User
from .forms import SignUpForm


def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'reg.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/home/')

