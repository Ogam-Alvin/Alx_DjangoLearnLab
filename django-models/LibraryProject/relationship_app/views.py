from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(
        request,
        'relationship_app/list_books.html',  # 🔴 MUST be this exact string
        {'books': books}
    )
