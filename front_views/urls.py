from django.urls import path
from front_views.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),

]
