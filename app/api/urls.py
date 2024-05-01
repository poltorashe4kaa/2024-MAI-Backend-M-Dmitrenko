from django.urls import path
from .views import *

urlpatterns = [
    path('categories', categories, name='categories'),
    path('search', search, name='search'),
    path('create', create_book, name='create_book'),
    path('', index, name='index')
]
