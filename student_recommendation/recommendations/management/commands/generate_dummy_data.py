from django.core.management.base import BaseCommand
from recommendations.views import generate_dummy_data

class Command(BaseCommand):
    help = "Generates and stores dummy data for students, courses, and grades."

    def handle(self, *args, **kwargs):
        generate_dummy_data()
        self.stdout.write(self.style.SUCCESS("Dummy data generated successfully!"))