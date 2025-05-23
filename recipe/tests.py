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

    def test_main_view_displays_latest_five_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipes']), 5)
        self.assertIn(self.recipe6, response.context['recipes'])
        self.assertIn(self.recipe5, response.context['recipes'])
        self.assertIn(self.recipe4, response.context['recipes'])
        self.assertIn(self.recipe3, response.context['recipes'])
        self.assertIn(self.recipe2, response.context['recipes'])
        self.assertNotIn(self.recipe1, response.context['recipes'])

    def test_main_view_recipe_content_in_html(self):
        response = self.client.get(reverse('main'))
        self.assertContains(response, self.recipe5.title)
        self.assertContains(response, self.recipe5.description)
        self.assertContains(response, self.recipe5.ingredients)
        self.assertContains(response, self.recipe5.instructions)
        self.assertContains(response, self.recipe5.category.name)


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.category_a = Category.objects.create(name='Category A')
        self.category_b = Category.objects.create(name='Category B')
        self.category_c = Category.objects.create(name='Category C')

        Recipe.objects.create(title='Recipe 1', description='Desc', instructions='Inst', ingredients='Ing', category=self.category_a)
        Recipe.objects.create(title='Recipe 2', description='Desc', instructions='Inst', ingredients='Ing', category=self.category_a)
        Recipe.objects.create(title='Recipe 3', description='Desc', instructions='Inst', ingredients='Ing', category=self.category_b)
        Recipe.objects.create(title='Recipe 4', description='Desc', instructions='Inst', ingredients='Ing', category=self.category_b)
        Recipe.objects.create(title='Recipe 5', description='Desc', instructions='Inst', ingredients='Ing', category=self.category_b)

    def test_category_list_view_uses_correct_template(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')

    def test_category_list_view_displays_all_categories_with_recipe_counts(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

        categories_in_context = response.context['categories']
        self.assertEqual(len(categories_in_context), 3)

        category_a_from_context = next(c for c in categories_in_context if c.name == 'Category A')
        self.assertEqual(category_a_from_context.recipe_count, 2)

        category_b_from_context = next(c for c in categories_in_context if c.name == 'Category B')
        self.assertEqual(category_b_from_context.recipe_count, 3)

        category_c_from_context = next(c for c in categories_in_context if c.name == 'Category C')
        self.assertEqual(category_c_from_context.recipe_count, 0)

        self.assertContains(response, 'Category A')
        self.assertContains(response, '<span class="badge bg-primary rounded-pill">2</span>')
        self.assertContains(response, 'Category B')
        self.assertContains(response, '<span class="badge bg-primary rounded-pill">3</span>')
        self.assertContains(response, 'Category C')
        self.assertContains(response, '<span class="badge bg-primary rounded-pill">0</span>')

    def test_category_list_view_empty_categories(self):
        Category.objects.all().delete()
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Categories')
        self.assertContains(response, 'No categories found.')
        self.assertNotContains(response, 'Category A')