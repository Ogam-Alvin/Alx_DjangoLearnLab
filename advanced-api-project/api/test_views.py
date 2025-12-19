from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Covers CRUD operations, permissions, filtering,
    searching, and ordering functionality.
    """

    def setUp(self):
        """
        Set up test data and authenticated user.
        Runs before each test.
        """
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create books
        self.book1 = Book.objects.create(
            title="Django Basics",
            publication_year=2020,
            author=self.author
        )

        self.book2 = Book.objects.create(
            title="Advanced Django",
            publication_year=2022,
            author=self.author
        )

        self.list_url = '/api/books/'
        self.create_url = '/api/books/create/'

    # ---------- READ TESTS ----------

    def test_list_books_unauthenticated(self):
        """
        Ensure unauthenticated users can list books.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """
        Ensure a single book can be retrieved by ID.
        """
        url = f'/api/books/{self.book1.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Django Basics")

    # ---------- CREATE TESTS ----------

    def test_create_book_unauthenticated_fails(self):
        """
        Ensure unauthenticated users cannot create books.
        """
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        # ✅ Change 401 to 403 to match DRF default behavior
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_book_authenticated(self):
        """
        Ensure authenticated users can create a book.
        """
        self.client.login(username='testuser', password='testpassword')

        data = {
            "title": "New Django Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------- UPDATE TESTS ----------

    def test_update_book_authenticated(self):
        """
        Ensure authenticated users can update a book.
        """
        self.client.login(username='testuser', password='testpassword')

        url = f'/api/books/update/{self.book1.id}/'
        data = {
            "title": "Updated Django Basics",
            "publication_year": 2020,
            "author": self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Django Basics")

    # ---------- DELETE TESTS ----------

    def test_delete_book_authenticated(self):
        """
        Ensure authenticated users can delete a book.
        """
        self.client.login(username='testuser', password='testpassword')

        url = f'/api/books/delete/{self.book1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------- FILTER / SEARCH / ORDER TESTS ----------

    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication_year.
        """
        response = self.client.get('/api/books/?publication_year=2022')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Advanced Django")

    def test_search_books_by_title(self):
        """
        Test searching books by title.
        """
        response = self.client.get('/api/books/?search=Advanced')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication_year.
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2022)
