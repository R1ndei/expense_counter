from django.shortcuts import render
import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ExpenseForm, UpdateForm
from .models import Expense, Category
from userpreferences.models import UserPreference
import datetime


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Expense.objects.filter(category__name__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


class ExpensesView(ListView):
    template_name = 'expenses/index.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency'] = UserPreference.objects.get(user=self.request.user).currency
        return context


class AddExpensesView(CreateView):
    form_class = ExpenseForm
    template_name = 'expenses/add_expense.html'
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateExpenseView(UpdateView):
    model = Expense
    form_class = UpdateForm
    template_name = 'expenses/edit-expense.html'
    success_url = reverse_lazy('expenses')
    context_object_name = 'expense'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteExpenseView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expenses')


def expense_category_summary(request):
    todays_day = datetime.date.today()
    six_months_ago = todays_day - datetime.timedelta(days=30 * 6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_day)
    finalrep = {}

    def get_category(expense):
        return expense.category.pk

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def statsView(request):
    return render(request, 'expenses/stats.html')
