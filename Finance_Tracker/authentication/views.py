from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from .forms import UserRegistrationForm, LoginForm
from expenses.models import Expenses, Liabilities

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        expenses_by_category = (
            Expenses.objects.filter(user=request.user)
            .values("category")
            .annotate(total_amount=Sum("amount"))
        )
        categories = [expense["category"] for expense in expenses_by_category]
        amounts = [expense["total_amount"] for expense in expenses_by_category]

        liab_by_category = (
            Liabilities.objects.filter(user=request.user)
            .values("category")
            .annotate(total_amount=Sum("amount"))
        )
        liab_categories = [liab["category"] for liab in liab_by_category]
        liab_amounts = [liab["total_amount"] for liab in liab_by_category]

        recent_expenses = Expenses.objects.filter(user=request.user).order_by("-date")[:5]

        context = {
            "categories": json.dumps(categories),
            "amounts": json.dumps(amounts),
            "liab_categories": json.dumps(liab_categories),
            "liab_amounts": json.dumps(liab_amounts),
            "recent_expenses": recent_expenses
        }
        print(context)
        return render(request, "home.html", context)
    return redirect('signin')





@csrf_exempt
def update_charts(request):
    if request.method == "POST":
        data = json.loads(request.body)

        start_date = data.get("start_date")
        end_date = data.get("end_date")
        range_option = data.get("range")

        if range_option:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=int(range_option) * 30)
        elif start_date and end_date and not range_option:
            start_date = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
            end_date = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
        else:
            return JsonResponse({"error": "Invalid date range"}, status=400)

        # Fetch filtered expense data
        expenses = (
            Expenses.objects.filter(date__range=[start_date, end_date], user=request.user)
            .values("category")  # Group by category
            .annotate(total_amount=Sum("amount"))  # Sum the amounts
            .order_by("category")  # Optional: Sort by category
        )
        expense_categories = [expense["category"] for expense in expenses]
        expense_amounts = [expense["total_amount"] for expense in expenses]

        # Fetch filtered liability data
        liabilities = (
            Liabilities.objects.filter(date__range=[start_date, end_date], user=request.user)
            .values("category")  # Group by category
            .annotate(total_amount=Sum("amount"))  # Sum the amounts
            .order_by("category")  # Optional: Sort by category
        )
        liab_categories = [liability["category"] for liability in liabilities]
        liab_amounts = [liability["total_amount"] for liability in liabilities]

        return JsonResponse({
            "expense_categories": expense_categories,
            "expense_amounts": expense_amounts,
            "liab_categories": liab_categories,
            "liab_amounts": liab_amounts,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.userprofile.first_name = form.cleaned_data["first_name"]
            user.userprofile.last_name = form.cleaned_data["last_name"]
            user.userprofile.email = form.cleaned_data["email"]
            user.userprofile.address = form.cleaned_data["address"]
            user.userprofile.Phonenumber = form.cleaned_data["phone_number"]
            user.userprofile.age = form.cleaned_data["age"]
            user.userprofile.sex = form.cleaned_data["sex"]
            
            if form.cleaned_data.get("image"):
                user.userprofile.image = form.cleaned_data["image"]

            user.save()
            return redirect('signin')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {
        'form': form
    })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("home")  # Change to your actual dashboard URL
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('signin')


