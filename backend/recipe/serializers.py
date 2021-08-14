import re
from django.core.exceptions import RequestAborted
from django.db.models import fields
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Favorite, Follow, Ingredient, IngredientItem, Recipe, Tag


User = get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['pk', 'title', 'colour', 'slug']


class FollowSerializer(serializers.ModelSerializer):
    