from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import NotificationViewSet, EpidemieAPIView, IncendieAPIView, InnondationAPIView, SecuriteAPIView
from .views import user_dashboard, admin_dashboard, stats_api

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # Dashboards
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    
    # API
    path('api/', include(router.urls)),
    path('api/stats/', stats_api, name='stats_api'),
    path('api/evacuation/epidemie/', EpidemieAPIView.as_view()),
    path('api/evacuation/incendie/', IncendieAPIView.as_view()),
    path('api/evacuation/innondation/', InnondationAPIView.as_view()),
    path('api/evacuation/securite/', SecuriteAPIView.as_view()),
]

