from django.urls import path
from core import views as core_views


urlpatterns = [
    path('', core_views.HomeView.as_view(), name='home'),
    path('about/', core_views.AboutView.as_view(), name='about'),
    path('contact/', core_views.ContactView.as_view(), name='contact'),
    path('learn-more/', core_views.LearnMoreView.as_view(), name='learn-more'),

    path('profile/', core_views.ProfileView.as_view(), name='profile'),
    path('create_budget', core_views.CreateBudgetView.as_view(), name='create_budget'),
    path('create_expense', core_views.CreateHistoricalExpenseView.as_view(), name='create_expense'),
    path('budget/<int:pk>', core_views.BudgetView.as_view(), name='budget'),
    path('statistics/<int:pk>', core_views.BudgetStats.as_view(), name='statistics'),
    path('show_stats', core_views.ShowStatistics.as_view(), name='show_stats'),

]
