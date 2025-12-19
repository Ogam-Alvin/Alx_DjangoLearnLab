from django.db import models

# Create your models here.
# Author model represents a writer who can have multiple books
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model represents a book written by an author
# Each book belongs to exactly one author (one-to-many relationship)
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()

    # ForeignKey establishes relationship: one Author → many Books
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title