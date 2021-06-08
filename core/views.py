from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from core.forms import CreateBudgetForm
from expenses.models import Budget, Expense
from expenses.serializers import ExpenseSerializer


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class LearnMoreView(TemplateView):
    template_name = 'learnmore.html'


class ProfileView(LoginRequiredMixin ,View):
    def get(self, request):
        own_budgets = Budget.objects.filter(created_by=request.user)
        member_budgets = Budget.objects.filter(users=request.user)
        context = {
            'own_budgets': own_budgets,
            'member_budgets': member_budgets,
        }

        return render(request, 'logged/profile.html', context)


class BudgetView(LoginRequiredMixin, DetailView):
    template_name = 'budget.html'
    model = Budget

    def get(self, request, pk):
        serializer = ExpenseSerializer()
        budget = Budget.objects.get(id=pk)
        expenses = Expense.objects.filter(budget=budget).order_by('-created_at')

        context = {
            'serializer': serializer,
            'budget': budget,
            'expenses': expenses,
        }

        return render(request, 'logged/budget.html', context)


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


