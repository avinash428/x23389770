from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Expenses(models.Model):
    CATEGORY_CHOICES = (
        ('Food', 'Food',),
        ('Rent', 'Rent',),
        ('Entertainment', 'Entertainment',),
        ('Car', 'Car',),
        ('Gym', 'Gym',),
        ('Subscriptions', 'Subscriptions',),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    amount = models.FloatField(null=False)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.amount}"
    

class Liabilities(models.Model):
    CATEGORY_CHOICES = [
        ("Loan", "Loan"),
        ("Credit Card", "Credit Card"),
        ("Mortgage", "Mortgage"),
        ("Car Loan", "Car Loan"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    amount = models.FloatField(null=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(null=False)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.amount}"





