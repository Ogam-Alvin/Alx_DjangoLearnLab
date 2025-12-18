from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import permission_required
from django.views.decorators.clickjacking import xframe_options_deny
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        # ORM automatically escapes input, safe from SQL injection
        books = Book.objects.filter(title__icontains=search_query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})



def form_example(request):
    form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})