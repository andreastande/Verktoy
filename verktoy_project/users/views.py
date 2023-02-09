from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages


# Create your views here.

#https://docs.djangoproject.com/en/4.1/topics/auth/default/#how-to-log-a-user-in
#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def signup(request):
    if request.method == 'POST': #når man sender skjema
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1') #hashet passord
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
        else:
            print("Invalid form")
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = UserCreationForm #når man laster inn login siden først
    return render(request, 'users/signup.html', {'form': form})

@login_required
def my_profile(request):
    current_user = request.user
    context = {'user': current_user}
    return render(request, 'users/my_profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profilen din ble oppdatert')
            return redirect('users:my_profile')
        
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form': profile_form}
    return render(request, 'users/update_profile.html', context)
