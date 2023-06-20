# temp/views.py
from .models import Temp
from .serializer import TempSerializer
from rest_framework import viewsets
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class TempViewSet(viewsets.ModelViewSet):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Temp.objects.all()
    serializer_class = TempSerializer
   
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)