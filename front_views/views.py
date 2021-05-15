from django.shortcuts import render
from django.views.generic import View

from expenses.models import Budget


class HomeView(View):

    def get(self, request):
        context = {
            'budget': Budget.objects.all()
        }

        return render(request, 'index.html', context)
