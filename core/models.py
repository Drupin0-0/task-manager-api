from django.db import models
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your models here.


class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipes_lideradas')
    membros = models.ManyToManyField(User, related_name='equipe_participantes')
    
    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    description = models.TextField()
    responsavel = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    data_limite = models.DateField()
    concluida = models.BooleanField(default=False)
    
class DeletarEquipeView(APIView):
    def delete(self, request, pk):
        try:
            equipe = Equipe.objects.get(pk=pk)
            equipe.delete
            return Response({'mensagem': 'Equipe deletada com sucesso!'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response ({'mensagem': 'Equipe nao encontrada!'}, status=status.HTTP_404_NOT_FOUND)