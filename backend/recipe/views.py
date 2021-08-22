from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientNameFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingList, Subscribe, Tag
from .paginators import PageNumberPaginatorModified
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeListSerializer, ShoppingListSerializer, SubscribersSerializer,
    SubscribeSerializer, TagSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    pagination_class = PageNumberPaginatorModified

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return CreateRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    search_fields = ['name', ]
    filter_class = IngredientNameFilter


@api_view(['get'])
def show_subscribes(request):
    user_obj = User.objects.filter(following__user=request.user)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = SubscribersSerializer(
        result_page,
        many=True,
        context={'current_user': request.user}
    )
    return paginator.get_paginated_response(serializer.data)


class SubscribeView(APIView):

    def get(self, request, user_id):
        user = request.user
        data = {
            'user': user.id,
            'author': user_id
        }
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        follow = get_object_or_404(
            Subscribe,
            user=user,
            author_id=user_id
        )
        follow.delete()
        return Response('Подписка удалена', status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(APIView):

    def get(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        favorite_recipe = get_object_or_404(
            Favorite,
            user=user,
            recipe__id=recipe_id
        )
        favorite_recipe.delete()
        return Response(
            'Рецепт удален из избранного',
            status.HTTP_204_NO_CONTENT
        )


class ShoppingListView(APIView):

    def get(self, request, recipe_id):
        user = request.user.id
        data = {
            'user': user,
            'recipe': recipe_id
        }
        serializer = ShoppingListSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        shopping_list_recipe = get_object_or_404(
            ShoppingList,
            user=user,
            recipe__id=recipe_id
        )
        shopping_list_recipe.delete()
        return Response(
            'Рецепт удален',
            status.HTTP_204_NO_CONTENT
        )


class ShoppingListDownload(APIView):

    def get(self, request):
        shopping_cart = request.user.shopping.all()
        shopping_list = {}
        for shopping in shopping_cart:
            ingredients = shopping.recipe.ingredientrecipe_set.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                unit = ingredient.ingredient.measurement_unit
                if name not in shopping_list:
                    shopping_list[name] = {
                        'amount': amount,
                        'unit': unit
                    }
                else:
                    shopping_list[name]['amount'] = (shopping_list[name]
                                                     ['amount'] + amount)
        wishlist = []
        for item in shopping_list:
            wishlist.append(f'{item} ({shopping_list[item]["unit"]}) — '
                            f'{shopping_list[item]["amount"]} \n\n')
        wishlist.append('Дипломный проект: FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wishlist.pdf"'
        return response
