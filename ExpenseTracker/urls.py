from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('expenses/', include('expenses.urls')),
    path('account/', include('account.urls')),
    path('', include('core.urls')),

]
