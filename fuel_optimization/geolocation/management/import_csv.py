import csv
from django.core.management.base import BaseCommand
from geolocation.models import FuelStation

class Command(BaseCommand):
    help = "Import fuel stations from a CSV file."

    def handle(self, *args, **kwargs):
        with open('fuel-prices-for-be-assessment.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                FuelStation.objects.create(
                    truckstop_id=row['OPIS Truckstop ID'],
                    truckstop_name=row['Truckstop Name'],
                    address=row['Address'],
                    city=row['City'],
                    state=row['State'],
                    retail_price=float(row['Retail Price'])
                )
        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
