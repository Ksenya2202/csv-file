import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from work_with_database.models import Phone

class Command(BaseCommand):
    help = 'Импортирует телефоны из CSV-файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV-файлу')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                Phone.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'price': row['price'],
                        'image': row['image'],
                        'release_date': datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                        'lte_exists': row['lte_exists'].lower() == 'true',
                    }
                )
        self.stdout.write(self.style.SUCCESS('Телефоны успешно загружены!'))
