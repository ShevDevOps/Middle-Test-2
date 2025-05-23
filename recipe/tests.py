from django.test import TestCase
from django.urls import reverse
from .models import Category, Recipe


class MainViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Desserts')
        self.category2 = Category.objects.create(name='Main Courses')

        self.recipe1 = Recipe.objects.create(
            title='Chocolate Cake',
            description='chocolate cake',
            instructions='Bake it!',
            ingredients='Chocolate',
            category=self.category1,
            created_at='2025-01-01T12:00:00Z'
        )
        self.recipe2 = Recipe.objects.create(
            title='Pasta Carbonara',
            description='pasta',
            instructions='Cook pasta',
            ingredients='Pasta',
            category=self.category2,
            created_at='2025-01-02T12:00:00Z'
        )
        self.recipe3 = Recipe.objects.create(
            title='Caesar Salad',
            description='salad',
            instructions='Mix',
            ingredients='Lettuce',
            category=self.category2,
            created_at='2025-01-03T12:00:00Z'
        )
        self.recipe4 = Recipe.objects.create(
            title='Apple Pie',
            description='apple pie',
            instructions='apples',
            ingredients='Apples',
            category=self.category1,
            created_at='2025-01-04T12:00:00Z'
        )
        self.recipe5 = Recipe.objects.create(
            title='Beef Stew',
            description='beef stew',
            instructions='cook beef',
            ingredients='Beef',
            category=self.category2,
            created_at='2025-01-05T12:00:00Z'
        )
        self.recipe6 = Recipe.objects.create(
            title='Lemon Bars',
            description='lemon bars',
            instructions='lemon',
            ingredients='Lemons',
            category=self.category1,
            created_at='2025-01-06T12:00:00Z'
        )

    def test_main_view_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    