$(document).ready(function() {
    var tabela = [];
    carrega_dados(tabela);

    $('#table_cadastro_usuario').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "columns": [
            {"data": "Username"},
            {"data": "Email"},
            {"data": "Data de inclusão"},
            {"data": "Último login"},
            {"data": "Excluir?"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(dados).forEach(k =>{

        dict_linhas['Username'] =  dados[k][1];
        dict_linhas['Email'] = dados[k][2];
        dict_linhas['Data de inclusão'] = dados[k][3];
        dict_linhas['Último login']= dados[k][4]
        dict_linhas['Excluir?']= '<div class="container-sm" align="center">' +
                               '<a id="exclui_' + dados [k][0] +
                               '" class="btn botao_excluir href="deleta_usuarios/" onclick="exclui_usuario(id)">Excluir</a>' +
                               '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}


function exclui_usuario(id){
    $.ajax({
        url: "/deleta_usuario/",
//        dataType: 'json',
        data: {'id_usuario': id},
        success: function(){
            location.reload();
        }
    })
}



