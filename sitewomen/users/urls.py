from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = "users"

urlpatterns = [
  path('login/', views.LoginUser.as_view(), name="login"), #users:login
  path('register/', views.RegisterUser.as_view(), name="register"), #users:register
  
  path('password-change/', views.UserPasswordChange.as_view(), name="password_change"), #users:password_change
  path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"), #users:password_change_done
  
  path('password-reset/', PasswordResetView.as_view(
    template_name="users/password_reset_form.html",
    email_template_name="users/password_reset_email.html",
    success_url=reverse_lazy("users:password_reset_done")
    ), name="password_reset"), #users:password_reset
  path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"), #users:password_reset_done
  
  path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    template_name="users/password_reset_confirm.html",
    success_url=reverse_lazy("users:password_reset_complete")
    ), name="password_reset_confirm"), #users:password_confirm
  path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"), #users:password_reset_complete
  
  path('profile/', views.ProfileUser.as_view(), name="profile"), #users:profile
  path('logout/', LogoutView.as_view(), name="logout"), #users:logout
]