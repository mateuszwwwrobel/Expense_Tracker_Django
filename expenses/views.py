from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from expenses.models import Expense, Budget
from expenses.serializers import ExpenseSerializer


class ExpenseListView(ListAPIView):
    queryset = Expense.objects.order_by('-created_at')
    serializer_class = ExpenseSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )


class ExpenseDetailView(RetrieveAPIView):
    queryset = Expense.objects.order_by('-created_at')
    serializer_class = ExpenseSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )


class ExpenseCreateView(CreateAPIView):
    serializer_class = ExpenseSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )


class ExpenseUpdateView(UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny,)


class ExpenseDeleteView(DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny,)


class TestView(View):

    def get(self, request):

        context = {
            'budget': Budget.objects.all(),
            'expenses': Expense.objects.filter(budget=1)
        }

        return render(self.request, 'index.html', context)
