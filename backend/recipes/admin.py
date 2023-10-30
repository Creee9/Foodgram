from django.contrib.admin import ModelAdmin, register
from .models import (
    Tag, Ingredient, Recipe, IngredientRecipe,
    ShoppingCart, Favorite, TagRecipe,
)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'author', 'name', 'text',
                    'cooking_time', 'created')
    serch_filter = ('author', 'name', 'tags',)
    list_filter = ('tags',)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


@register(IngredientRecipe)
class IngredientRecipe(ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


@register(TagRecipe)
class TagRecipeAdmin(ModelAdmin):  # поправил
    list_display = ('pk', 'tag', 'recipe')
