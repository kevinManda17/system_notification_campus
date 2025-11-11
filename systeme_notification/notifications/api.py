from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from .core import Epidemie, Incendie, Innondation, Securite

# ViewSet pour notifications
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# ViewSets pour chaque urgence (API pour déclencher evacuer)
from rest_framework.views import APIView
from rest_framework.response import Response

class EpidemieAPIView(APIView):
    def post(self, request):
        e = Epidemie()
        e.evacuer()
        return Response({"status": "Epidemie evacuation déclenchée"})

class IncendieAPIView(APIView):
    def post(self, request):
        i = Incendie()
        i.evacuer()
        return Response({"status": "Incendie evacuation déclenchée"})

class InnondationAPIView(APIView):
    def post(self, request):
        n = Innondation()
        n.evacuer()
        return Response({"status": "Innondation evacuation déclenchée"})

class SecuriteAPIView(APIView):
    def post(self, request):
        s = Securite()
        s.evacuer()
        return Response({"status": "Sécurité evacuation déclenchée"})
