from django.shortcuts import render
from django.views.generic import TemplateView, View


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class LearnMoreView(TemplateView):
    template_name = 'learnmore.html'


class CreateBudgetView(View):

    def get(self, request):
        return render(request, 'logged/create_budget.html')
