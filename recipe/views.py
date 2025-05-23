from .models import Recipe, Category
from django.shortcuts import render

def main(request):
    recipes = Recipe.objects.all()[:5]
    return render(request, 'main.html', {'recipes': recipes})