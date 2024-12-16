# your_app/management/commands/populate_ecotracking.py

from django.core.management.base import BaseCommand
from system.models import EcoTrackingData
from django.contrib.auth.models import User
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Populate EcoTrackingData with sample data'

    def handle(self, *args, **kwargs):
        # Fetch users
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Please create users first.'))
            return
        
        # Create sample data
        for user in users:
            for _ in range(10):  # Create 10 entries per user
                EcoTrackingData.objects.create(
                    user=user,
                    carbon_footprint=random.uniform(100.0, 500.0),  # Random float between 100 and 500
                    energy_consumption=random.uniform(50.0, 300.0),  # Random float between 50 and 300
                    water_usage=random.uniform(10.0, 100.0),  # Random float between 10 and 100
                    date=date.today() - timedelta(days=random.randint(1, 30))  # Random date in the last 30 days
                )
        self.stdout.write(self.style.SUCCESS('Sample eco-tracking data populated successfully.'))
