from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render, get_object_or_404
from login.models import User
from .forms import EditProfileForm
from .models import Company


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # otherwise user will have to login again
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home/profile')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changePassword.html', {
        'form': form,
        'username': request.user.username,
    })


@login_required()
def home_view(request):
    username = None
    companies = None
    if request.user.is_authenticated:
        username = request.user.username
        companies = Company.objects.all()
    context = {
        'username': username,
        'companies': companies
    }
    return render(request, 'Home.html', context)


@login_required()
def update_profile(request, id=None):
    instance = get_object_or_404(User, id=request.user.id)
    form = EditProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get("username"))
        instance.save()
        messages.success(request, 'Profile details updated!')
        return redirect('/home/profile')
    context = {
        'instance': instance,
        'form': form,
        'username': request.user.username,
    }
    return render(request, "editProfile.html", context)


@login_required()
def profile_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        user = User.objects.get(username=username)
        phone_number = user.phone_number

        if not first_name:
            first_name = "None"
        if not last_name:
            last_name = "None"
        if not phone_number:
            phone_number = "None"
        context = {
            'username': username,
            'first_name': first_name,
            'email': email,
            'last_name': last_name,
            'phone_number': phone_number,

        }

        return render(request, 'userProfile.html', context)
