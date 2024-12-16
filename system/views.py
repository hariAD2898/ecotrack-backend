
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EcoTrackingData,EcoGoal
from .serializers import EcoTrackingSerializer,EcoGoalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from django.db.models.functions import TruncDate
from django.db import connection
from rest_framework.views import APIView
class EcoTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        eco_data = EcoTrackingData.objects.filter(user=request.user)
        serializer = EcoTrackingSerializer(eco_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EcoTrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EcoGoalViewSet(viewsets.ModelViewSet):
    queryset = EcoGoal.objects.all()
    serializer_class = EcoGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure that only goals related to the logged-in user are returned
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the logged-in user as the owner of the goal
        serializer.save(user=self.request.user)


class EcoTrackingDailyProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Use raw SQL for date truncation compatible with SQLite
            daily_data = EcoTrackingData.objects.filter(user=request.user) \
                .annotate(day=RawSQL("date(date)", ())) \
                .values('day') \
                .annotate(
                    total_carbon_footprint=Sum('carbon_footprint'),
                    total_energy_consumption=Sum('energy_consumption'),
                    total_water_usage=Sum('water_usage')
                ).order_by('day')

            # Print the actual SQL query for debugging
            print(connection.queries[-1])  # Shows the most recent query executed

            return Response(daily_data)

        except Exception as e:
            print(f"Error fetching daily progress: {e}")
            return Response({'error': 'Error fetching daily progress data'}, status=500)
