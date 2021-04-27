from django.contrib.auth.models import User
from django.test import TestCase
from expenses.models import Expense


class TestExpenseModel(TestCase):

    def setUp(self) -> None:
        user_1 = User.objects.create(username='testuser')
        user_1.set_password('testpassword')
        user_1.save()
        self.expense_1 = Expense.objects.create(
            user=user_1,
            amount=123,
            currency='PLN',
            category='Food',
        )

    def test_get_by_id_method(self) -> None:
        found_expense = Expense.get_by_id(self.expense_1.id)
        not_found_expense = Expense.get_by_id(123123)
        self.assertEqual(not_found_expense, None)
        self.assertEqual(found_expense, self.expense_1)
