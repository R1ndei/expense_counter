from django.forms import ModelForm, TextInput, Select
from expenses.models import Expense
from userincome.models import UserIncome


class IncomeForm(ModelForm):
    class Meta:
        model = UserIncome
        fields = ['amount', 'description', 'source', 'date']
        widgets = {
            'amount': TextInput(attrs={'class': "form-control form-control-sm"}),
            'description': TextInput(attrs={'class': "form-control form-control-sm"}),
            'source': Select(attrs={'class': "form-control"}),
            'date': TextInput(attrs={'class': "form-control form-control-sm", 'type': 'date'}),
        }


class UpdateIncomeForm(ModelForm):
    class Meta:
        model = UserIncome
        fields = ['amount', 'description', 'source', 'date']
        widgets = {
            'amount': TextInput(attrs={'class': "form-control form-control-sm"}),
            'description': TextInput(attrs={'class': "form-control form-control-sm"}),
            'source': Select(attrs={'class': "form-control"}),
            'date': TextInput(attrs={'class': "form-control form-control-sm", 'type': 'date'}),
        }
