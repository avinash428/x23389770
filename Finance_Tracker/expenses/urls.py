from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    view_expenses,
    edit_expense,
    delete_expense,
    liabilities,
    edit_liability,
    delete_liability

)


urlpatterns = [
    path('expenses/', view_expenses, name='expenses_view'),
    path('expense/edit/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('expense/delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    
    path("liabilities/", liabilities, name="liabilities"),
    path("liabilities/edit/<int:liability_id>/", edit_liability, name="edit_liability"),
    path("liabilities/delete/<int:liability_id>/", delete_liability, name="delete_liability"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)