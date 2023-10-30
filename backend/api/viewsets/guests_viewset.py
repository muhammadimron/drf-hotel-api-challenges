from rest_framework import authentication, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.authentication import BearerAuthentication
from api.models import Guest
from api.serializers import GuestSerializer

class GuestViewSets(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["GET"], detail=False)
    def add(self, request, *args, **kwargs):
        Guest.objects.all().delete()
        for i in range(1, 11):
            serializer = GuestSerializer(data={
                "name": f"People number {i}",
                "email": f"people{i}@gmail.com"
            })
            serializer.is_valid()
            serializer.save()
        return Response({
            "success": "please hit http://127.0.0.1:8000/guests/ to see the result."
        }, status=status.HTTP_200_OK)

