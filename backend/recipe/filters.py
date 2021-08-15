from django.db.models import fields
import django_filters as filters

from .models import Ingredient, Recipe


class IngredientTitleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='title', lookup_expr='istartwith')

    class Meta:
        model = Ingredient
        fields = ('name', 'dimension')
    

class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
