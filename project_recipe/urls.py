from django.contrib import admin
from django.urls import path
from recipe.views import category_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('category_list/', category_list, name="categories")
]