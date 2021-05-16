from django.urls import path
from core.views import HomeView, AboutView, ContactView, BeginView, LearnMoreView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('about/', AboutView.as_view(), name='about-page'),
    path('contact/', ContactView.as_view(), name='contact-page'),
    path('begin/', BeginView.as_view(), name='begin-page'),
    path('learn-more/', LearnMoreView.as_view(), name='learn-more-page'),

]
