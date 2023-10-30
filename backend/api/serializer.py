from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag, TagRecipe)
from rest_framework import serializers
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser, Follow

# ---------------------------------------------------------------------
#             Работа с пользователями и моделью CustomUser
# ---------------------------------------------------------------------


class CustomUserSerializer(UserCreateSerializer):
    """Сериализатор для полученя списка пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        """Метод для проверки подписки на пользователей"""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomCreateUserSerializer(CustomUserSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


# -----------------------------------------------------------------------
#                          Рецепты, теги и ингридиенты
# -----------------------------------------------------------------------

class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для описания ингридиентов в рецепте"""

    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:

        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    """Сериализатор для полученя рецептов"""

    ingredients = IngredientRecipeSerializer(source='ingredient_recipe',
                                             many=True)
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        "Метод, проверяющий подписку"

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        "Метод, проверяющий наличие рецепта в корзине"

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe=obj).exists()


class IngredientRecipeCreateSerializer(ModelSerializer):
    """Сериализатор для создания ингридиентов в рецептах"""

    id = IntegerField()
    amount = IntegerField()

    class Meta:

        model = IngredientRecipe
        fields = ('id', 'amount')

    @staticmethod
    def validate_amount(value):
        """Метод для проверки количества ингридиента"""

        if value < 1:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть не меньше 1'
            )
        return value


# class Base64ImageField(serializers.ImageField):
#     """Кодирования картинок base64"""

#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

#         return super().to_internal_value(data)


class CreateRecipeSerializer(ModelSerializer):
    """Сериализатор для создания рецепта"""

    ingredients = IngredientRecipeCreateSerializer(many=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField(use_url=True)

    class Meta:

        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        """Метод для проверки ингридиентов и тегов"""

        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        list_ingredients = []
        list_tags = []

        if not ingredients or not tags:
            raise serializers.ValidationError('Списки ингредиентов и тегов \
                                              не должны быть пустыми')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError('Такого ингридиента нет')

            if ingredient['id'] in list_ingredients:
                raise serializers.ValidationError(
                    'Ингридиенты не должны повторяться'
                )
            list_ingredients.append(ingredient['id'])
        for tag in tags:
            if tag in list_tags:
                raise serializers.ValidationError(
                    'Теги не должны повторяться'
                )
            list_tags.append(tag)

        return data

    def to_representation(self, instance):
        """Метод для преобразования типа данных"""

        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )

        return serializer.data

    def create_ingredients(self, ingredients, recipe):
        """Методы для создания ингридиента"""

        for ingr in ingredients:
            id = ingr['id']
            ingredient = Ingredient.objects.get(pk=id)
            amount = ingr['amount']
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )

    def create_tags(self, tags, recipe):
        """Метод для добавления тега"""

        recipe.tags.set(tags)

    def create(self, validated_data):
        """Метод для создания модели"""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Метод обновления модели"""

        IngredientRecipe.objects.filter(recipe=instance).delete()
        TagRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        self.create_tags(validated_data.pop('tags'), instance)

        return super().update(instance, validated_data)

# ---------------------------------------------------------------------------
#                                  Подписки и избранное
# ---------------------------------------------------------------------------


class FirstFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow"""

    class Meta:
        model = Follow
        fields = ('author', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'user'),
                message='Вы уже подписывались на этого автора'
            )
        ]

    def validate(self, data):
        """Проверяем, что пользователь не подписывается на самого себя."""
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data


class ForFollowRecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов для FollowSerializer"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    """Сериализатор для отображение в подписке"""

    recipes = SerializerMethodField(read_only=True, method_name='get_recipes')
    recipes_count = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        """Метод для получения рецептов"""

        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ForFollowRecipeSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        """Метод для получения количества рецептов"""

        return obj.recipes.count()


class FavoritSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления в избранное"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        """Метод для проверки ингридиентов и тегов"""

        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError('Такого ингридиента нет')
        return data
