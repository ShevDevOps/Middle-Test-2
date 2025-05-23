from django.contrib import admin
from django.urls import path
from recipe.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
]