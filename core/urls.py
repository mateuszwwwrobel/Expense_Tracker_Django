from django.urls import path
from core import views as core_views


urlpatterns = [
    path('', core_views.HomeView.as_view(), name='home'),
    path('about/', core_views.AboutView.as_view(), name='about'),
    path('contact/', core_views.ContactView.as_view(), name='contact'),
    path('learn-more/', core_views.LearnMoreView.as_view(), name='learn-more'),

    path('profile/', core_views.ProfileView.as_view(), name='profile'),
    path('create_budget', core_views.CreateBudgetView.as_view(), name='create_budget'),

]
