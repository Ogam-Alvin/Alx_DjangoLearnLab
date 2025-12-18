from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
]
