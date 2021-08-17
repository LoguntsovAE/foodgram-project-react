import django_filters as filters

from .models import Ingredient, Recipe


class IngredientTitleFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tag__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tag')
