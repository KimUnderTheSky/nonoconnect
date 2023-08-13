from django.urls import path
from .views import *

app_name = "account"

urlpatterns = [
    path("login", account_Login.as_view(), name="login"),

    path("logout", account_Logout.as_view(), name="logout"),
    
    path("signup", account_Signup.as_view(), name = "signup"),
]
