from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from staff.models import Address
from user.forms import LoginForm, RegisterForm, UserForm

User = get_user_model()


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            request.session['invalid_user'] = True

    return render(request, 'login.html', {'login_form': form})


@login_required(login_url='/user/login')  # Check login
def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        password_again = form.cleaned_data.get('password_again')
        email = form.cleaned_data.get('email')
        firstname = form.cleaned_data.get('first_name')
        lastname = form.cleaned_data.get('last_name')
        full_address = form.cleaned_data.get('full_address')
        city = form.cleaned_data.get('city')
        country = form.cleaned_data.get('country')
        try:
            address = Address.objects.create(
                city=city,
                country=country,
                full_address=full_address
            )

            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                password=password,
                email=email,
                address=address
            )
        except:
            user = None
            address = None
        if user and address is not None:
            login(request, user)
            return redirect('/')
        else:
            request.session['registration_error'] = True

    return render(request, 'register.html', {'register_form': form})


@login_required(login_url='/user/login')  # Check login
def account_details_view(request):
    user_form = UserForm(instance=request.user)
    return render(request, 'account.html', {'user_form': user_form})
