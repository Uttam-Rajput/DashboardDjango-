import json
from django.core.management.base import BaseCommand
from mainApp.models import DataEntry

class Command(BaseCommand):
    help = "Import JSON data into MongoDB"

    def handle(self, *args, **kwargs):
        try:
            with open("jsondata.json", "r", encoding="utf-8") as file:
                data = json.load(file)  # Load JSON data

            # Insert data into MongoDB
            for entry in data:
                DataEntry.objects.create(
                    end_year=int(entry["end_year"]) if entry["end_year"] else None,
                    topic=entry.get("topic", ""),
                    sector=entry.get("sector", ""),
                    region=entry.get("region", ""),
                    pestle=entry.get("pestle", ""),
                    source=entry.get("source", ""),
                    swot=entry.get("swot", ""),
                    country=entry.get("country", ""),
                    city=entry.get("city", ""),
                    intensity=int(entry["intensity"]) if entry["intensity"] else None,
                    likelihood=int(entry["likelihood"]) if entry["likelihood"] else None,
                    relevance=int(entry["relevance"]) if entry["relevance"] else None,
                )

            self.stdout.write(self.style.SUCCESS("Data imported successfully!"))

        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON format error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))
