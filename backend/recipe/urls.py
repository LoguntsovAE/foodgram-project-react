from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingListDownload, ShoppingListView, SubscribeView,
                    TagViewSet, show_subscribes)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/subscriptions/',
         show_subscribes, name='users_subs'),
    path('users/<int:user_id>/subscribe/',
         SubscribeView.as_view(), name='subscribe'),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='add_recipe_to_favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingListView.as_view(), name='add_recipe_to_shopping_cart'),
    path('recipes/download_shopping_cart/',
         ShoppingListDownload.as_view(), name='dowload_shopping_cart'),
    path('', include(router.urls))
]
