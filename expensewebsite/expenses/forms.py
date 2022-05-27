from django.forms import ModelForm, TextInput, Select
from expenses.models import Expense



class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date']
        widgets = {
            'amount': TextInput(attrs={'class': "form-control form-control-sm"}),
            'description': TextInput(attrs={'class': "form-control form-control-sm"}),
            'category': Select(attrs={'class': "form-control"}),
            'date': TextInput(attrs={'class': "form-control form-control-sm", 'type': 'date'}),
                   }


class UpdateForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date']
        widgets = {
            'amount': TextInput(attrs={'class': "form-control form-control-sm"}),
            'description': TextInput(attrs={'class': "form-control form-control-sm"}),
            'category': Select(attrs={'class': "form-control"}),
            'date': TextInput(attrs={'class': "form-control form-control-sm", 'type': 'date'}),
             }





