from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View
from core.forms import CreateBudgetForm


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class LearnMoreView(TemplateView):
    template_name = 'learnmore.html'


class ProfileView(TemplateView):
    template_name = 'logged/profile.html'


class CreateBudgetView(LoginRequiredMixin, View):

    def get(self, request):
        form = CreateBudgetForm()
        context = {
            'form': form,
        }

        return render(request, 'logged/create_budget.html', context)

    def post(self, request):
        form = CreateBudgetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()

        return render(request, 'logged/create_budget.html')


