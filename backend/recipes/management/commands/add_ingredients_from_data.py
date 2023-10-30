import csv
from django.core.management.base import BaseCommand
from foodgram.settings import CSV_FILES_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки ингредиентов в базу данных """

    def import_ingredients_from_csv_file(self, *args, **kwargs):
        with open(f'{CSV_FILES_DIR}/ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)

    def handle(self, *args, **options):
        self.import_ingredients_from_csv_file()
