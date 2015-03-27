from django.core.management.base import BaseCommand
from app.models import Product
import csv

class Command(BaseCommand):
    args = ''
    help = ''

    def _populate_db(self):
        import os
        with open(os.path.join('app', 'management', 'commands', 'grocery.csv'), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                p = Product(name=row[0], price=row[1], image_link=row[2], description=row[3])
                p.save()

    def handle(self, *args, **options):
        self._populate_db()
