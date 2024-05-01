from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
# Create your views here.

def register(request):
    if request.method == 'POST':
        # Get form data from POST request
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        # Perform basic validation
        if email and password1 and password2:
            if password1 == password2:
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return redirect('signin')
                else:
                    error_message = "This email address is already registered."
            else:
                error_message = "Passwords do not match."
        else:
            error_message = "All fields are required."

        # If any error occurred, render the registration form with error message
        return render(request, 'accounts/register.html', {'error_message': error_message})

    # If it's a GET request, render the registration form without any error
    return render(request, 'accounts/register.html')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            print("all good")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                streamlit_url = 'http://localhost:8501/'
                streamlit_url += f'?username={user.username}&email={user.email}'     
                return redirect(streamlit_url)
            else:
                error_message = "Invalid username or password. Please try again."
                return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form submission. Please try again."
            return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})

    return render(request, 'accounts/login.html')


def signout(request):
    print('aa to raha hai')
    auth_logout(request)
    return JsonResponse({'message': 'Successfully logged out'})


def check_login_status(request):
    print('here')
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})
    
def get_user_data(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_data = {
                'user':request.user,
                'username': request.user.username,
                'email': request.user.email,
                # Add more user data as needed
            }
            return JsonResponse(user_data)
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
