from django.urls import path
from .views import *

from django.urls import path
from .views import *

urlpatterns = [
    path('categories', categories, name='categories'),
    path('search', search, name='search'),
    path('create', create_book, name='create_book'),
    path('', index, name='index'),
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('register', register_user, name='register_user'),
    path('add_favorite_book', add_favorite_book, name='add_favorite_book'),
    path('get_favorites', get_favorites, name='get_favorites'),
    path('create_category', create_category, name='create_category'),
    path('delete_favorite_book', delete_favorite_book, name='delete_favorite_book'),
]
