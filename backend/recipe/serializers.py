from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Follow, Ingredient, IngredientItem, Recipe,
                     ShoppingList, Tag)

User = get_user_model


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'colour', 'slug']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ['user', 'author']

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(User, pk=author.get('id'))
        user = validated_data.get('user')
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя'
            )
        if Follow.objects.filter(
                author=author,
                user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны'
            )
        return Follow.objects.create(user=user, author=author)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        obj, created = Favorite.objects.get_or_create(user=user,
                                                      recipe=recipe)
        if not created:
            raise serializers.ValidationError(
                {
                    "message": "Нельзя добавить повторно в избранное"
                }
            )
        return validated_data


class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = ShoppingList
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        recipe = validated_data['recipe']
        obj, created = ShoppingList.objects.get_or_create(user=user,
                                                          recipe=recipe)
        if not created:
            raise serializers.ValidationError(
                {"message": "Вы уже добавили рецепт в корзину"}
            )
        return validated_data


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientItemSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(
        source='ingredient.name', read_only=True
    )
    dimension = serializers.ReadOnlyField(
        source='ingredient.dimension', read_only=True
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = IngredientItem
        fields = ['id', 'title', 'quantity', 'dimension']


class IngredientItemCreate(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    def to_representation(self, instance):
        return IngredientItemSerializer(
            IngredientItem.objects.get(ingredient=instance.id)
        ).data


class RecipeSerializer(serializers.ModelSerializer):
    liked = serializers.SerializerMethodField()
    in_shopping_list = serializers.SerializerMethodField()
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                             many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientItemCreate(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tag', 'author', 'ingredient', 'liked',
            'in_shopping_list', 'title', 'image', 'description',
            'cooking_time', 'pub_date'
        ]

    def get_liked(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(user=request.user,
                                           recipe=obj).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredient')
        tag_data = validated_data.pop('tag')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tag.set(tag_data)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            if amount < 1:
                raise serializers.ValidationError(
                    'Убедитесь, что это значение больше 0.'
                )
            ingredient_instance = get_object_or_404(Ingredient,
                                                    pk=ingredient.get('id'))
            IngredientItem.objects.create(recipe=recipe,
                                          ingredient=ingredient_instance,
                                          amount=amount)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredient')
        tag_data = validated_data.pop('tag')
        recipe = Recipe.objects.filter(id=instance.id)
        recipe.update(**validated_data)
        ingredients_instance = [
            ingredient for ingredient in instance.ingredient.all()
        ]
        for item in ingredients_data:
            amount = item['amount']
            ingredient_id = item['id']
            if amount < 1:
                raise serializers.ValidationError(
                    'Убедитесь, что это значение больше 0.'
                )
            if IngredientItem.objects.filter(
                    id=ingredient_id, amount=amount
            ).exists():
                ingredients_instance.remove(
                    IngredientItem.objects.get(id=ingredient_id,
                                               amount=amount).ingredient)
            else:
                IngredientItem.objects.get_or_create(
                    recipe=instance,
                    ingredient=get_object_or_404(Ingredient, id=ingredient_id),
                    amount=amount
                )
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image', instance.image)
        instance.ingredients.remove(*ingredients_instance)
        instance.tags.set(tag_data)
        return instance


class RecipeReadSerializer(RecipeSerializer):
    tag = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredient = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredient = IngredientItem.objects.filter(recipe=obj)
        return IngredientItemSerializer(ingredient, many=True).data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'image', 'cooking_time']


class ShowFollowsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return RecipeSubscriptionSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return queryset.count()
