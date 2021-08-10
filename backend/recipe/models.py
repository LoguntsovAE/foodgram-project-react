from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

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
    title = models.CharField(
        'Название ингридиента',
        max_length=100
    )
    dimension = models.CharField(
        'Еденица измерения',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'dimension'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.title


class IngredientItem(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingrediens',
        verbose_name='Ингредиенты'
    )
    quantity = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),)
    )

    class Meta:
        vaerbose_name = 'Ингредиент связь'
        vaerbose_name_plural = 'Ингредиент связи'

    def __str__(self):
        return self.ingredient.title
