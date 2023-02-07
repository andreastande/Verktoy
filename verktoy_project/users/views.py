from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


# Create your views here.

def home(request): #placeholder
    return render(request, 'users/home.html')

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
