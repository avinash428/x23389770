from django import forms
from django.core.exceptions import ValidationError

from .models import Expenses, Liabilities

CATEGORY_CHOICES = (
        ('F', 'Food',),
        ('R', 'Rent',),
        ('E', 'Entertainment',),
        ('C', 'Car',),
        ('G', 'Gym',),
        ('S', 'Subscriptions',),
    )

class ExpensesRegistrationForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['name', 'amount', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LiabilityForm(forms.ModelForm):
    class Meta:
        model = Liabilities
        fields = ["name", "amount", "category", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }