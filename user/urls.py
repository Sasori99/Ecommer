from django.urls import path

from user.views import login_view, register_view, logout_view, account_details_view

urlpatterns = [
    path('user/login', login_view, name="login"),
    path('user/register', register_view, name="register"),
    path('user/logout', logout_view, name="logout"),
    path('user/details', account_details_view, name="account-details"),
]
