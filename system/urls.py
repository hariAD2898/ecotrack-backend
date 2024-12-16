from django.urls import path,include
from .views import EcoTrackingView,EcoGoalViewSet,EcoTrackingDailyProgressView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'eco-goals', EcoGoalViewSet, basename='eco-goals')

urlpatterns = [
    path('eco-tracking/', EcoTrackingView.as_view(), name='eco-tracking'),
    path('eco-tracking/daily-progress/', EcoTrackingDailyProgressView.as_view(), name='eco-tracking-daily-progress'),

    path('', include(router.urls)),
]
