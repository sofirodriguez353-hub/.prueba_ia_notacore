from django.contrib.auth import views as auth_views
from django.urls import path

from .views import CustomPasswordChangeView, LoginView, LogoutView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
        name="password_change_done",
    ),
]
