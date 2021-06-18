from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelChoiceField
from django.utils.translation import ugettext_lazy as _
from staff.models import Address

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'password']
        labels = {
            'first_name': _('Họ'),
            'last_name': _('Tên'),
            'last_login': _('Lần đăng nhập cuối'),
            'username': _('Tên tài khoản'),
            'email': _('Email'),
            'date_joined': _('Ngày tham gia'),
            'address': _('Địa chỉ')
        }

    disabled_fields = ['date_joined', 'last_login', 'address']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            attrs = {'class': 'form-row'}
            if field in self.disabled_fields:
                attrs['readonly'] = 'readonly'
            self.fields[field].widget.attrs.update(attrs)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-row'})
    )

    def clean(self):
        cleanned_username = self.clean_username()
        cleanned_password = self.cleaned_data.get('password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)

        if not qs.exists():
            raise forms.ValidationError("User already exists")

        return username


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-row'})
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-row'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    full_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-row'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please choose another")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("This email is already in use")
        return email

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password')

        if not password == password_again:
            raise forms.ValidationError("Password does not match")
        return password
