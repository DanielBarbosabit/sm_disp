from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

urlpatterns = [
    path('', views.index),
    path(r'index/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cria_cadastro', views.cria_cadastro, name='cria_cadastro'),
    path(r'dashboard/', views.dashboard, name='dashboard'),
    path(r'busca_dados_atuais/', views.atualiza_pizza),
    path(r'logout/', views.logout, name='logout'),
    path('cadastrardispenser/', views.cadastrardispenser, name='cadastrardispenser'),
    path('cadastrousuarios/', views.cadastrousuarios, name='cadastro_usuarios'),
    path('deleta_usuario/', views.deletausuarios, name='deleta_usuarios'),
    path('habilita_broker/', views.habilita_broker, name='habilita_broker'),
    path('desabilita_broker/', views.desabilita_broker, name='desabilita_broker'),
    path('adddispenser/', views.adiciona_dispenser, name='adddispenser'),
    path('deleta_dispenser/', views.deleta_dispenser, name = 'deletar_dispenser'),
    path('edita_dispenser/', views.edita_dispenser, name='edita_disperser'),
    path('visao_logs/', views.visao_logs, name = 'visao_logs'),
    path('exporta_logs/', views.exporta_logs, name = 'exporta_logs'),
    path('edeleta_logs/', views.deleta_logs, name = 'deleta_logs'),
    path('atualiza_logs/', views.atualiza_logs, name = 'atualiza_logs')
]

urlpatterns += staticfiles_urlpatterns()