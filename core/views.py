from datetime import datetime
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from core.forms import CreateBudgetForm
from django.contrib import messages
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


class ProfileView(LoginRequiredMixin, View):
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
            messages.success(request, 'Budget successfully created!')

        return render(request, 'logged/create_budget.html', {'form': CreateBudgetForm()})


class BudgetStats(LoginRequiredMixin, View):

    def get(self, request, pk):
        budget = Budget.objects.get(id=pk)

        context = {
            'budget': budget,
        }

        return render(request, 'logged/budget_stats_select.html', context)


class ShowStatistics(LoginRequiredMixin, View):

    def get(self, request):
        budget_id = request.GET['budget']
        start_date = request.GET['start']
        end_date = request.GET['end']

        budget = Budget.objects.get(id=budget_id)

        if end_date != '':
            s_year = int(start_date[:4])
            s_month = int(start_date[-2:])
            e_year = int(end_date[:4])
            e_month = 1 if end_date[-2:] == 12 else int(end_date[-2:])

            expenses = Expense.objects.filter(budget=budget).\
                filter(created_at__gte=datetime(s_year, s_month, 1)).\
                filter(created_at__lt=datetime(e_year, e_month + 1, 1))
        else:
            year = start_date[:4]
            month = start_date[-2:]

            expenses = Expense.objects.filter(budget=budget).\
                filter(created_at__year=year).\
                filter(created_at__month=month)

        chart_1_data = self.get_percentage_chart_data(expenses)

        context = {
            'budget': budget,
            'expenses': expenses,
            'chart_1_data': chart_1_data,
        }

        return render(request, 'logged/budget_stats_show.html', context)

    @staticmethod
    def get_percentage_chart_data(queryset):
        expense_percentage = dict(queryset.values_list('category').annotate(total_price=Sum('price')))
        total_expenses = queryset.aggregate(sum=Sum('price'))

        dataset = {}
        for category, amount in expense_percentage.items():
            percentage = (100 * amount) / total_expenses['sum']
            percentage = float(percentage)
            dataset[category] = round(percentage, 2)

        colors = []
        for color in range(len(expense_percentage)):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        data = {
            'labels': list(dataset.keys()),
            'data': list(dataset.values()),
            'colors': colors,
        }
        return data
