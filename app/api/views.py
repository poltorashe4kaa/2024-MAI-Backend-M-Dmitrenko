from django.shortcuts import render
from .models import *
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def categories(request):
    categories = Category.objects.all()
    data = serializers.serialize('json', categories)
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
        if categories:
            print(categories)
            for category_id in categories:
                category = Category.objects.filter(id=category_id).first()
                if category:
                    book.categories.add(category)
                else:
                    print(f"Категория с id={category_id} не найдена")
        book.save()
        return JsonResponse({'id': book.id, 'title': book.title, 'description': book.description})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def index(request):
    books = Book.objects.all()
    serialized_data = json.loads(serializers.serialize('json', books))
    return JsonResponse(serialized_data, safe=False)
# TODO: посмотреть как правильно делать авторизацию пользователей в Django.

# TODO: скачать постман и посмотреть пройдёт ли другое запросы кроме / , далее посмотреть всё  ли правильно в urls
# TODO: 