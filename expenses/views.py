from django.shortcuts import redirect
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from expenses.models import Expense
from expenses.serializers import ExpenseSerializer
from rest_framework.response import Response


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

    def create(self, request, *args, **kwargs):
        response = super(ExpenseCreateView, self).create(request, *args, **kwargs)

        return redirect('budget', pk=response.data['budget'])


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

    def delete(self, request, *args, **kwargs):
        super(ExpenseDeleteView, self).delete(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)
