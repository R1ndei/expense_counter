from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.ExpensesView.as_view(), name="expenses"),
    path('add-expense/', views.AddExpensesView.as_view(), name="add-expenses"),
    path('edit-expense/<int:pk>/', views.UpdateExpenseView.as_view(), name="expense-edit"),
    path('expense-delete/<int:pk>/', views.DeleteExpenseView.as_view(), name="expense-delete"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search_expenses"),
    path('expense_category_summary/', views.expense_category_summary, name="expense_category_summary"),
    path('stats', views.statsView, name="stats"),
]
