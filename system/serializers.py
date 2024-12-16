from rest_framework import serializers
from .models import EcoTrackingData,EcoGoal

class EcoTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoTrackingData
        fields = '__all__'


class EcoGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoGoal
        fields = '__all__'