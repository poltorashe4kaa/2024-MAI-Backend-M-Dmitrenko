from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.

def categories(request):
    categories = Category.objects.all()
    data = json.loads(serializers.serialize('json', categories))
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    data = json.loads(serializers.serialize('json', books))
    return JsonResponse(data, safe=False)


# @require_http_methods(["POST"])
@csrf_exempt
def create_book(request):
    if request.method == 'POST':
        print(request.body)
        json_data = json.loads(request.body)
        title = json_data.get('title')
        description = json_data.get('description')
        author = json_data.get("author")
        release_year = int(json_data.get("release_year"))
        categories = json_data.get("categories")
        print("release_year: " + str(release_year))
        book = Book(title=title, description=description, release_year=release_year, author=author)
        book.save()
        if categories:
            print(categories)
            for category_id in categories:
                category = Category.objects.filter(id=category_id).first()
                if category:
                    book.categories.add(category)
                else:
                    print(f"Категория с id={category_id} не найдена")
        
        return JsonResponse({'id': book.id, 'title': book.title, 'description': book.description})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def index(request):
    books = Book.objects.all()
    serialized_data = json.loads(serializers.serialize('json', books))
    return JsonResponse(serialized_data, safe=False)
# TODO: посмотреть как правильно делать авторизацию пользователей в Django.

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("login")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse('index'))
        else:
            return HttpResponse("Что-то не то с пользователем")
    else:
        return HttpResponse("Метод не POST")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Проверка на уникальность имени пользователя
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Пользователь с таким именем уже существует'}, status=400)

            # Создание нового пользователя
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Аутентификация и вход пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': 'Регистрация успешна'})
            else:
                return JsonResponse({'error': 'Ошибка при аутентификации'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)

@require_http_methods(["GET"])
def add_favorite_book(request): 
    if request.user.is_authenticated:
        user = request.user.profile
        book_id = request.GET.get('book_id')
        if not book_id:
            return JsonResponse({'error': 'Book ID is required'}, status=400)
        book = Book.objects.get(id=book_id)
        user.favorite_books.add(book)
        return JsonResponse({'success': 'Book added to favorites'})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

@require_http_methods(["GET"])
def get_favorites(request):
    if request.user.is_authenticated:
        user = request.user.profile
        favorite_books = user.favorite_books.all()
        data = json.loads(serializers.serialize('json', favorite_books))
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'success': 'User logged out'})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
@require_http_methods(["POST"])
@csrf_exempt
def create_category(request):
    data = json.loads(request.body)
    name = data.get('name')
    category = Category(name=name)
    category.save()
    return JsonResponse({'id': category.id, 'name': category.name})

@require_http_methods(["GET"])
@csrf_exempt
def delete_favorite_book(request):
    if request.user.is_authenticated:
        user = request.user.profile
        book_id = request.GET.get('book_id')
        if not book_id:
            return JsonResponse({'error': 'Book ID is required'}, status=400)
        book = Book.objects.get(id=book_id)
        user.favorite_books.remove(book)
        return JsonResponse({'success': 'Book removed from favorites'})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)