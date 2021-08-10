from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(
        'Рецепт',
        max_length=100
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipe_photo/',
        blank=True, null=True
    )
    description = models.TextField(
        'Описание'
    )
    ingredient = models.ManyToManyField(
        'Ingredient',
        through='IngredientItem',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Ингридиент', max_length=100)
