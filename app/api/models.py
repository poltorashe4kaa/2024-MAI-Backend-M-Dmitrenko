from django.db import models

# Create your models here.

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    author = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='books', blank=True)

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    favorite_books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name




