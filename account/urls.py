from django.urls import path
from account import views as account_views

urlpatterns = [
    path('begin/', account_views.BeginView.as_view(), name='begin'),

    path('signup/', account_views.SignUpView.as_view(), name='signup'),
    path('login/', account_views.LoginView.as_view(), name='login'),
    path('logout/', account_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', account_views.ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-sent/', account_views.password_reset_sent, name='password-reset-sent'),

    path('account-activation-send/', account_views.account_activation_sent, name='account-activation-sent'),
    path('activate/<uidb64>/<token>/', account_views.activate, name='activate'),

]
