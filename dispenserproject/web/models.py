from django.db import models
from django.contrib.auth.models import User

#tabela de logs dos dispenser
class Logs(models.Model):
    topico_dispenser = models.CharField(max_length=30, null=False)
    date_time = models.CharField(max_length=20, null=False)
    battery_level = models.IntegerField(null=False)
    paper_level = models.IntegerField(null=False)

#tabela de identificacao dos dispensers e seu relacionamento
class Ident_dispenser(models.Model):
    topico_dispenser = models.CharField(max_length=50, null=False)
    client_id_mqtt = models.CharField(max_length=30, null=False)
    localizacao = models.CharField(max_length=200, null=True)
    id_usuario_id = models.IntegerField(null=True)
    #campos para acumulo de papel
    relacao_pacotes = models.IntegerField(default=100)
    porcentagem_acumulada = models.IntegerField(default=0)
    paper_level_last = models.IntegerField(default=0)
    ultima_atualizacao = models.CharField(max_length=20,default='null')

#Tabela dos históricos de pacotes completos em determinada data por dispenser
class Historico_pacotes(models.Model):
    topico_dispenser = models.CharField(max_length=30, null=False)
    date_time = models.CharField(max_length=20, null=False)