from django.shortcuts import render
from .models import Category
from django.db.models import Count

def category_list(request):
    categories = Category.objects.annotate(recipe_count=Count('categories'))
    return render(request, 'category_list.html', {'categories': categories})
