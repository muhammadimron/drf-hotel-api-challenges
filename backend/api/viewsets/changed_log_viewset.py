from rest_framework import viewsets, authentication, permissions
from api.authentication import BearerAuthentication
from api.models import ChangedLog
from api.serializers import ChangedLogSerializer

class ChangedLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChangedLog.objects.all()
    serializer_class = ChangedLogSerializer
    lookup_field = "pk"
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]