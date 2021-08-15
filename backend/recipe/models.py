from django.contrib.auth import get_user_model
from django.db import models

from colorfield.fields import ColorField

User = get_user_model()


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
        ordering = ['title']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        unique_together = ['title', 'dimension']

    def __str__(self):
        return f'{self.title}({self.dimension})'


class Tag(models.Model):
    title = models.CharField(
        max_length=15,
        verbose_name='Тег',
        help_text='Введите название тега',
        unique=True
    )
    slug = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Уникальный слаг',
        help_text='Введите название слага',
        unique=True,
    )
    colour = ColorField(
        null=True,
        verbose_name='colour HEX',
        help_text='Введите цвет в HEX',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


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
        help_text = 'Загрузить изображение'
    )
    description = models.TextField(
        'Описание',
        max_length=1000
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientItem',
        # through_fields=('recipe', 'ingredient'),
    )
    tag = models.ManyToManyField(
        Tag,
        'Теги',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class IngredientItem(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Ингредиент",
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        null=True,
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избарнное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'user: {self.user.username}, recipe: {self.recipe.title}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'user: {self.user.username}, recipe: {self.recipe.title}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор на кого подписались'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['author', 'user']

    def __str__(self):
        return (
            f'Подписчик: {self.user.username} подписан на автора: {self.author.title}'
        )
