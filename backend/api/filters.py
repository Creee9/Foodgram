import django_filters
from django_filters.filters import ModelMultipleChoiceFilter, NumberFilter
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    """Фильтр по названию"""

    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(django_filters.FilterSet):
    """ Фильтр избранного и списка покупок"""

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = NumberFilter(
        method='is_recipe_in_favorites_filter'
    )
    is_in_shopping_cart = NumberFilter(
        method='is_recipe_in_shoppingcart_filter'
    )

    def is_recipe_in_favorites_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(favoriting__user_id=user.id)
        return queryset

    def is_recipe_in_shoppingcart_filter(self, queryset, name, value):
        if value == 1:
            user = self.request.user
            return queryset.filter(shopping_cart__user_id=user.id)
        return queryset

    class Meta:

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
