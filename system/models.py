from django.db import models
from django.contrib.auth.models import User

class EcoTrackingData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='system_ecotrackingdata')
    carbon_footprint = models.FloatField()
    energy_consumption = models.FloatField()
    water_usage = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class EcoGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_goals')
    goal_type = models.CharField(max_length=255)  # E.g., 'carbon_footprint', 'energy_consumption', 'water_usage'
    target_value = models.FloatField()  # The target value the user wants to achieve
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()  # Deadline for the goal
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s {self.goal_type} goal"