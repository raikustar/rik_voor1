import csv
from django.core.management.base import BaseCommand
from osauhingud.models import Osauhing

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file") 

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            next(reader)
            for row in reader:
                Osauhing.objects.create(
                    companyname = row["companyname"],
                    registrycode = row["registrycode"],
                    foundingdate = row["foundingdate"],
                    totalcapital = row["totalcapital"]
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
