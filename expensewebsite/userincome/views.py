from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from userincome.models import Source, UserIncome
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   UserIncome.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   UserIncome.objects.filter(description__icontains=search_str, owner=request.user) | \
                   UserIncome.objects.filter(source__icontains=search_str, owner=request.user)

        data = incomes.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        data = request.POST['income_date']
        source = request.POST['source']

        if not amount or not description or not source:
            messages.error(request, "Some field is empty")
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, description=description, date=data,
                                  source=source)
        messages.success(request, "Income save successfully")
        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        data = request.POST['income_date']
        source = request.POST['source']

        if not amount or not description or not source:
            messages.error(request, "Some field is empty")
            return render(request, 'income/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = data
        income.source = source
        income.save()
        messages.success(request, "Income updated successfully")
        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Success delete")
    return redirect('income')
