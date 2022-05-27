from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.IncomeView.as_view(), name="income"),
    path('add-income/', views.AddIncomeView.as_view(), name="add-income"),
    path('edit-income/<int:pk>/', views.UpdateIncomeView.as_view(), name="income-edit"),
    path('income-delete/<int:pk>/', views.DeleteIncomeView.as_view(), name="income-delete"),
    path('search-income/', csrf_exempt(views.search_income), name="search_income"),
]
