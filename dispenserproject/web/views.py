from django.shortcuts import render, redirect
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time
from time import time as timer
from apscheduler.schedulers.background import BackgroundScheduler
from web.models import Logs, Ident_dispenser
from django.http import HttpResponse, JsonResponse
import random
from django.contrib.auth.models import User
from django.contrib import auth, messages
import datetime
from django.contrib.auth.models import User
from django.db import connection
import json
import csv
# from web.model_forms import Cadastro_dispenser

#Declaração de variáveis globais
global bConnected
bConnected = False
global tempo_coleta
tempo_coleta = []

# Quantidade maxima de linhas na tabela de log
global max_linhas
max_linhas = 5000

#Intervalo de coleta com o broker
global intervalo_coleta
intervalo_coleta = 10

sched = BackgroundScheduler()

def callback_broker():

    start = timer()

    # Chama rotina para verificação da quantidade de registro da tabela de LOGS
    busca_e_salva = verifica_qtde_logs()

    if busca_e_salva:
        # Conexão simples com o Broker
        print("Abrindo conexão...")
        try:
            msg = subscribe.simple("sdtx0000001", hostname="broker.hivemq.com",
                                   port=1883, keepalive = 10, client_id="smartdispenserws")

            topico_dispenser = str(msg.topic)
            battery_level = str(msg.payload).strip("b'")[0:3]
            battery_level = int(battery_level)
            papel_level = str(msg.payload).strip("b'")[3:6]
            if papel_level == '00Z':
                papel_level = 0
            elif papel_level == '00C':
                papel_level = 1000
            else:
                papel_level = int(papel_level)

            date_time = datetime.datetime.now()
            date_time = date_time.strftime("%m/%d/%Y-%H:%M:%S")


            new_data = Logs(topico_dispenser = topico_dispenser, date_time=date_time,
                                      battery_level = battery_level, paper_level = papel_level)
            new_data.save()
            print("Dado inserido no banco de dados")

        except:
            print("Não coletada a mensagem")
    else:
        print('Banco de dados já atingiu o máximo estipulado')


def habilita_broker(request):
    if sched.state == 2:
        sched.resume()
        return redirect('dashboard')
    if sched.state == 1:
        return redirect('dashboard')
    # Schedule job_function to be called every two hours
    sched.add_job(callback_broker, 'interval', seconds=intervalo_coleta)
    sched.start()
    return redirect('dashboard')

def desabilita_broker(request):
    if sched.state == 1:
        sched.pause()
        return redirect('dashboard')
    else:
        return redirect('dashboard')

def index(request):

    return render(request, 'inicial.html')

def login(request):
    # """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email'].strip()
        senha = request.POST['senha'].strip()
        if email == '' and senha == '':
            messages.error(request,'Os campos email e senha não podem ficar em branco')
            return redirect('/index/')
        elif email == '':
            messages.error(request,'O campos email não pode ficar em branco')
            return redirect('/index/')
        elif senha == '':
            messages.error(request,'O campos senha não pode ficar em branco')
            return redirect('/index/')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
        else:
            messages.error(request,'Usuário/Senha inválidos')
            return redirect('/index/')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    return render(request, 'cadastro.html')

def cria_cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome'].strip()
        email = request.POST['email'].strip()
        senha = request.POST['password'].strip()
        senha2 = request.POST['password2'].strip()
        if not nome:
            messages.error(request,'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if not email:
            messages.error(request,'O campo email não pode ficar em branco')
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request,'Usuário já cadastrado')
            return redirect('cadastro')
        if email == 'daniel_herbert_barbosa@hotmail.com' or email == 'diogom382@gmail.com':
            user = User.objects.create_user(username=nome, email=email, password=senha, is_superuser=True)
            user.save()
            messages.error(request, 'Usuário cadastrado com sucesso!')
            return redirect('index')
        else:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()
            messages.error(request, 'Usuário cadastrado com sucesso!')
            return redirect('index')


def dashboard(request):
    if request.user.is_active:
        return render(request, 'dashboard.html')
    else:
        return render(request, '/index/')

#Views - Cadastrar dispenser
def busca_info_dispenser():
    # JSON da relação de dispensers e usuário
    query = connection.cursor()
    query_str = """
         select
             d.topico_dispenser, a.email, d.localizacao
         from
             web_ident_dispenser d
         inner join
             auth_user a
         on
             a.id = d.id_usuario_id;
     """
    query.execute(query_str)
    dados_dispensers = query.fetchall()
    query.close()
    return dados_dispensers

def busca_usuarios():
    # JSON da relação com todos os usuários
    query = connection.cursor()
    query_str = """
        select 
            a.id, a.email 
        from 
            auth_user a;
    """
    query.execute(query_str)
    dados_usuarios = query.fetchall()
    query.close()
    return dados_usuarios

def cadastrardispenser(request):
    if request.user.is_superuser:
        try:
            dados_dispensers = busca_info_dispenser()
            dados_usuarios = dict(busca_usuarios())

            dados_dispensers = json.dumps(dados_dispensers)
            dados_usuarios = json.dumps(dados_usuarios)

        except:
            dados_dispensers = 'invalido'
            dados_usuarios = 'invalido'

        return render(request, 'cadastrardispenser.html', {'dados': dados_dispensers,
                                                           'usuarios': dados_usuarios})
    else:
        return render(request, 'dashboard/')

def adiciona_dispenser(request):
    #Verifica o último dispenser incluído
    try:
        ultimo_dispenser = Ident_dispenser.objects.order_by('-id')[0].id
    except:
        ultimo_dispenser = 0

    #Montagem da string do topico e client ID
    topico_new_dispenser = 'sdtx' + str(ultimo_dispenser + 1).zfill(9)
    client_new_dispenser = topico_new_dispenser

    if request.user.is_superuser:
        id_admin = auth.get_user(request).id

        #Inclusão do novo dispenser alocando-o para os administradores
        new_dispenser = Ident_dispenser(topico_dispenser = topico_new_dispenser,
                                        client_id_mqtt = client_new_dispenser,
                                        localizacao = 'null',
                                        id_usuario_id = id_admin)

        new_dispenser.save()

    return redirect('cadastrardispenser')

def deleta_dispenser(request):
    topico_deletado = request.GET['topico_dispenser'].split('_')[1]

    Ident_dispenser.objects.filter(topico_dispenser=topico_deletado).delete()

    return redirect('cadastrardispenser')

def edita_dispenser(request):
    if request.POST:
        dispenser = str(request.POST.get('id_dispenser'))
        localizacao = str(request.POST.get('localizacao_dispenser'))
        email = str(request.POST.get('email_usuario'))

        query = connection.cursor()
        query_str = "select a.id from auth_user a where a.email = '{}';".format(email)

        query.execute(query_str)
        id = query.fetchone()[0]
        query.close()

        #Edição do dispenser
        edited_dispenser = Ident_dispenser.objects.get(topico_dispenser = dispenser)
        edited_dispenser.localizacao = localizacao
        edited_dispenser.id_usuario_id = int(id)

        edited_dispenser.save()


    return redirect('cadastrardispenser')

#Views - Página de visão de Logs
def busca_logs():
    query = connection.cursor()
    query_str = """
         select 
             *
         from 
             web_logs;
     """
    query.execute(query_str)
    dados_logs = query.fetchall()
    query.close()

    return dados_logs

def visao_logs(request):

    dados_logs = json.dumps(busca_logs())

    return render(request, 'visao_logs.html', {'dados': dados_logs})

def exporta_logs(request):
    logs = busca_logs()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="logsdispenser.csv"'
    writer = csv.writer(response)
    writer.writerows(logs)

    return response

def deleta_logs(request):
    query = connection.cursor()
    query_str = """
         delete from web_logs;
     """
    query.execute(query_str)
    query.close()

    return redirect('visao_logs')


def atualiza_pizza(request):
    try:
        bateria_atual = Logs.objects.filter(topico_dispenser='sdtx0000001').order_by('-id')[0].battery_level
        nivel_papel_atual = Logs.objects.filter(topico_dispenser='sdtx0000001').order_by('-id')[0].paper_level

        nivel_papel_atual = nivel_papel_atual / 10
        bateria_atual = bateria_atual / 100
    except:
        nivel_papel_atual = random.randint(1,99)
        bateria_atual = 100


    return JsonResponse({'paper_level': nivel_papel_atual, 'baterry_level': bateria_atual})


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("RC da conexão: " + str(rc))
    print("Flags da conexão: " + str(flags))
    print("Cliente da conexão: " + str(client))
    print("Userdata da conexão: " + str(userdata))

def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload))

def worker_thread():
    """Creates mqtt client which check connection between pi and mqtt broker"""
    global bConnected
    client = mqtt.Client(client_id='smartdispenserws')
    client.on_message = on_message
    client.on_connect = on_connect
    time.sleep(1)
    while not bConnected:
        try:
            print ("Trying to connect broker")
            host = "test.mosquitto.org"
            porta = 1883
            client.connect(host=host, port=porta, keepalive=60)
            client.loop_start()
            client.on_message = on_message
            time.sleep(1)
            if client.is_connected():
                bConnected = True
                print("Cliente Broker está conectado")
        except:
            print("Cliente está desconectado")
            bConnected = False

    msg = subscribe.simple("smartdispenser_tx", hostname=host,port=porta)
    print("%s %s" % (msg.topic, msg.payload))
    client.loop_stop()


def verifica_qtde_logs():
    query = connection.cursor()
    query_str = """
        select 
            count(*)
        from
            web_logs;
    """
    query.execute(query_str)
    qtde_logs = int(query.fetchone()[0])
    query.close()

    if qtde_logs > max_linhas:
        return False

    return True
