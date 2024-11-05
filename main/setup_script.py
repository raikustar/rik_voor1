import os
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")  # Replace with your project's name
django.setup()

try:
    print("Running makemigrations...")
    call_command("makemigrations")
    
    print("Running migrate...")
    call_command("migrate")
    
    print("Running collectstatic...")
    call_command("collectstatic", interactive=False)  

    print("Importing data from CSV...")
    call_command("import_data", "./osauhingud/csv_data.csv") 
    
    print("All commands executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")