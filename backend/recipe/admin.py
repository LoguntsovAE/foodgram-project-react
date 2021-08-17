from django.contrib import admin
from import_export.admin import ImportMixin

from .models import (Favorite ,Follow, Ingredient,
                     IngredientItem, Recipe, Tag)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')


@admin.register(IngredientItem)
class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'recipe', 'quantity')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title')
    list_filter = ('title', 'tag', 'author')


@admin.register(Ingredient)
class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)
    resource_class = IngredientItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'colour')
    empty_value_display = 'empty'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')

