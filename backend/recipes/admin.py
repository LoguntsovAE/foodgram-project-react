from django.contrib import admin

from.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                    ShoppingList, Tag, Subscribe)


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInLine]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInLine]


admin.site.register(Favorite)
admin.site.register(IngredientRecipe)
admin.site.register(ShoppingList)
admin.site.register(Subscribe)
admin.site.register(Tag)
