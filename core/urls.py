from django.urls import path
from core import views as core_views

urlpatterns = [
    path('', core_views.HomeView.as_view(), name='home'),
    path('about/', core_views.AboutView.as_view(), name='about'),
    path('contact/', core_views.ContactView.as_view(), name='contact'),
    path('begin/', core_views.BeginView.as_view(), name='begin'),
    path('learn-more/', core_views.LearnMoreView.as_view(), name='learn-more'),

    path('signup/', core_views.SignUpView.as_view(), name='signup'),
    path('login/', core_views.LoginView.as_view(), name='login'),
    path('account_activation_send/', core_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', core_views.activate, name='activate'),


]
