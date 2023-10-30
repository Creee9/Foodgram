from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import CustomUser


class Tag(models.Model):
    """Модель для описания тегов"""

    name = models.CharField(
        max_length=200,
        verbose_name='тег',
        help_text='Введите название тега',
    )
    color = models.CharField(
        max_length=7,
        default='#569914',
        help_text='Введите цвет тега в формате HEX',
        validators=[
            RegexValidator(
                regex=r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Необходимо указать цвет в кодировке HEX.'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='уникальный слаг',
        help_text='Введите слаг',
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Слаг тега содержит недопустимый символ'
            )
        ]
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return f"{self.name}"


class Ingredient(models.Model):
    """Модель для описания ингридиентов"""

    name = models.CharField(
        max_length=200,
        verbose_name='название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}."


class Recipe(models.Model):
    """Модель для описания рецептов"""

    author = models.ForeignKey(
        CustomUser,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        verbose_name='фото рецепта',
    )
    text = models.TextField(
        verbose_name='описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        verbose_name='теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовлениия',
        validators=[
            MinValueValidator(1, message='Время приготовления: больше 1 мин.'),
        ]
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации рецепта',
    )

    class Meta:
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.name}"


class TagRecipe(models.Model):
    """Вспомогательный модель для описания тегов в рецептах"""

    recipe = models.ForeignKey(
        Recipe,
        related_name='tag_recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        related_name='tag_recipe',
        on_delete=models.CASCADE,
        verbose_name='тег',
        help_text='Тег',
    )

    class Meta:

        verbose_name = 'тег в рецепте'
        verbose_name_plural = 'теги в рецептах'

    def __str__(self):
        return f"{self.recipe} {self.tag}"


class IngredientRecipe(models.Model):
    """Вспомогательный модель для для связи ингредиентов и рецептов"""

    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='Выберите ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        help_text='Введите количество',
        validators=[MinValueValidator(1, message='Количество не меньше 1')]
    )

    class Meta:

        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return (f'Для рецепта {self.recipe} понадобится '
                f'{self.amount} {self.ingredient}')


class Favorite(models.Model):
    """Класс для добавления рецептов в избранное."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='рецепт'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    """Модель для составления списка покупок."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='пользователь'
    )

    class Meta:
        verbose_name = 'Рецепт пользователя для списка покупок'
        verbose_name_plural = 'Рецепты пользователей для списка покупок'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
