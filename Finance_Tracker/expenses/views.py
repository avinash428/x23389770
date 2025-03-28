from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required

from .models import Expenses, Liabilities
from .forms import ExpensesRegistrationForm, LiabilityForm

# Create your views here.

def view_expenses(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = ExpensesRegistrationForm(request.POST)
            if form.is_valid():
                expense = Expenses.objects.create(
                    user = request.user,
                    name=form.cleaned_data["name"],
                    amount=form.cleaned_data["amount"],
                    category=form.cleaned_data["category"],
                    date=form.cleaned_data["date"],
                )
            expense.save()
        form = ExpensesRegistrationForm()
        expenses = Expenses.objects.filter(user=request.user)
        return render(request, 'expenses.html', {"expenses":expenses, "form":form})
    return redirect('signin')


def edit_expense(request, expense_id):
    expense = get_object_or_404(Expenses, id=expense_id)
    if request.method == 'POST':
        form = ExpensesRegistrationForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses_view')
    else:
        form = ExpensesRegistrationForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expenses, id=expense_id)
    expense.delete()
    return redirect('expenses_view')


@login_required
def liabilities(request):
    if request.method == "POST":
        form = LiabilityForm(request.POST)
        if form.is_valid():
            liability = form.save(commit=False)
            liability.user = request.user
            liability.save()
            return redirect("liabilities")
    else:
        form = LiabilityForm()
        liabs = Liabilities.objects.filter(user=request.user)
    context = {
        "form": form,
        "liab": liabs
    }
    return render(request, "liabilities.html", context)

@login_required
def edit_liability(request, liability_id):
    liability = get_object_or_404(Liabilities, id=liability_id, user=request.user)

    if request.method == "POST":
        form = LiabilityForm(request.POST, instance=liability)
        if form.is_valid():
            form.save()
            return redirect("liabilities")
    else:
        form = LiabilityForm(instance=liability)

    return render(request, "edit_liability.html", {"form": form, "liability": liability})

@login_required
def delete_liability(request, liability_id):
    liability = get_object_or_404(Liabilities, id=liability_id, user=request.user)
    liability.delete()
    return redirect("liabilities")