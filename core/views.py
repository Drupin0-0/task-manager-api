from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from rest_framework.permissions  import IsAuthenticated
from .permissions import  IsLiderOrReadOnly
from .models import Tarefa, Equipe
from core.serializer import TarefaSerializer, EquipeSerializer, UserSerializer
# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['patch'], url_path='concluir')
    def concluir_tarefa(self, request, pk=None):
        tarefa = self.get_object()

        if tarefa.responsavel != request.user:
            return Response({'detail': 'Apenas o responsável pode concluir esta tarefa.'},
                            status=status.HTTP_403_FORBIDDEN)

        tarefa.concluida = True
        tarefa.save()
        return Response({'detail': 'Tarefa concluída com sucesso!'}, status=status.HTTP_200_OK)
    def get_queryset(self):
        user = self.request.user
        return Tarefa.objects.filter(equipe__membros=user)
class EquipeviewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [IsAuthenticated, IsLiderOrReadOnly ]
    