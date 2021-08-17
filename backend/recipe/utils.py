from import_export import resources

from .models import Ingredient


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ['pk', 'title', 'dimension']
