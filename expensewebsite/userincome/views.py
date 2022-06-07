from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from userincome.forms import IncomeForm, UpdateIncomeForm
from userincome.models import UserIncome
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse
import datetime
from django.views import View
from django.shortcuts import render


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                  UserIncome.objects.filter(date__istartswith=search_str, owner=request.user) | \
                  UserIncome.objects.filter(description__icontains=search_str, owner=request.user) | \
                  UserIncome.objects.filter(source__icontains=search_str, owner=request.user)

        data = incomes.values()
        return JsonResponse(list(data), safe=False)


class IncomeView(ListView):
    template_name = 'income/index.html'
    context_object_name = 'income'
    paginate_by = 10

    def get_queryset(self):
        return UserIncome.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency'] = UserPreference.objects.get(user=self.request.user).currency
        return context


class AddIncomeView(CreateView):
    form_class = IncomeForm
    template_name = 'income/add_income.html'
    success_url = reverse_lazy('income')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateIncomeView(UpdateView):
    model = UserIncome
    form_class = UpdateIncomeForm
    template_name = 'income/edit_income.html'
    success_url = reverse_lazy('income')
    context_object_name = 'income'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteIncomeView(DeleteView):
    model = UserIncome
    success_url = reverse_lazy('income')


class Income_source_summary(View):
    def get_amount_for_income(self, income_list, source):
        filtered_by_source = income_list.filter(source__name=source)
        amount = 0

        for i in filtered_by_source:
            amount += i.amount

        return amount

    def get(self, request):
        todays_day = datetime.date.today()
        six_months_ago = todays_day - datetime.timedelta(days=30 * 6)
        incomes = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_day)
        finalrep = {}
        source_list = list(set(map(lambda income: income.source.name, incomes)))

        for _ in incomes:
            for j in source_list:
                finalrep[j] = self.get_amount_for_income(incomes, j)

        return JsonResponse({'income_category_data': finalrep}, safe=False)


def statsView(request):
    return render(request, 'income/stats.html')