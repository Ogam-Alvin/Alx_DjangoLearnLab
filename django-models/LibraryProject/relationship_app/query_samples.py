from .models import Author, Book, Library, Librarian

# Example setup (optional)
author1 = Author.objects.create(name="George Orwell")
book1 = Book.objects.create(title="1984", author=author1)
book2 = Book.objects.create(title="Animal Farm", author=author1)

library1 = Library.objects.create(name="Central Library")
library1.books.add(book1, book2)

librarian1 = Librarian.objects.create(name="Alice", library=library1)

# --- Queries ---

# 1. All books by a specific author
books_by_orwell = Book.objects.filter(author__name="George Orwell")
print("Books by George Orwell:", books_by_orwell)

# 2. List all books in a library
books_in_central = library1.books.all()
print("Books in Central Library:", books_in_central)

# 3. Retrieve the librarian for a library
librarian_of_central = Librarian.objects.get(library__name="Central Library")
print("Librarian of Central Library:", librarian_of_central)
