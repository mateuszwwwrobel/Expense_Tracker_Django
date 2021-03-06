from datetime import datetime
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, DetailView
from core.forms import CreateBudgetForm, CreateHistoricalExpense
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
        expenses = Expense.objects.filter(budget=budget).order_by('-created_at')\
            .filter(created_at__month=datetime.today().month)

        context = {
            'serializer': serializer,
            'budget': budget,
            'expenses': expenses,
            'total_year': Expense.get_total_expenses_for_current_year(budget.id),
            'total_month': Expense.get_total_expenses_for_current_month(budget.id),
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


class CreateHistoricalExpenseView(LoginRequiredMixin, View):

    def get(self, request):
        user = {'user': request.user}
        form = CreateHistoricalExpense(user)
        context = {
            'form': form,
        }

        return render(request, 'logged/historical_expenses.html', context)

    def post(self, request):
        user = {'user': request.user}
        form = CreateHistoricalExpense(request.POST, user)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Expense successfully added.')
            return redirect('create_expense')

        else:
            messages.error(request, 'Please enter a correct date. YYYY-MM-DD')

        return render(
            request,
            'logged/historical_expenses.html',
            {'form': CreateHistoricalExpense(request.POST, user)}
        )


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
            e_year = int(end_date[:4]) if int(end_date[-2:]) != 12 else int(end_date[:4]) + 1
            e_month = 1 if int(end_date[-2:]) == 12 else (int(end_date[-2:])) + 1

            expenses = Expense.objects.filter(budget=budget).\
                filter(created_at__gte=datetime(s_year, s_month, 1)).\
                filter(created_at__lt=datetime(e_year, e_month, 1))

        else:
            year = start_date[:4]
            month = start_date[-2:]

            expenses = Expense.objects.filter(budget=budget).\
                filter(created_at__year=year).\
                filter(created_at__month=month)

        chart_1_data = self.get_chart_data_by_categories(expenses)
        chart_2_data = self.get_chart_data_by_users(expenses)
        agr_expenses = expenses.values('category').order_by('category').annotate(total_price=Sum('price'))

        context = {
            'budget': budget,
            'expenses': agr_expenses,
            'chart_1_data': chart_1_data,
            'chart_2_data': chart_2_data,
        }

        return render(request, 'logged/budget_stats_show.html', context)

    @staticmethod
    def get_chart_data_by_categories(queryset):
        expense_percentage = dict(queryset
                                  .values_list('category')
                                  .order_by('category')
                                  .annotate(total_price=Sum('price')))
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

    @staticmethod
    def get_chart_data_by_users(queryset):
        expense_percentage = dict(queryset
                                  .values_list('user')
                                  .order_by('user')
                                  .annotate(total_price=Sum('price')))
        total_expenses = queryset.aggregate(sum=Sum('price'))

        dataset = {}
        for user, amount in expense_percentage.items():
            percentage = (100 * amount) / total_expenses['sum']
            percentage = float(percentage)
            username = User.objects.get(id=user).username.capitalize()
            dataset[username] = round(percentage, 2)

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
