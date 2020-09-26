$(document).ready(function() {
    var tabela = [];
    carrega_dados(tabela);

    $('#table_logs_dispenser').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "order": [[ 1, "desc" ]],
        "columns": [
            {"data": "ID do log"},
            {"data": "Dispenser"},
            {"data": "Data"},
            {"data": "Tensão Baterial"},
            {"data": "Nível de papel"},
        ],
        "data": tabela,
        
    });
});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(dados).forEach(k =>{

        dict_linhas['ID do log'] =  dados[k][0];
        dict_linhas['Dispenser'] = dados[k][1];
        dict_linhas['Data'] = dados[k][2];
        dict_linhas['Tensão Baterial']= dados[k][3]
        dict_linhas['Nível de papel']= dados[k][4]
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}


function exclui_dispenser(id){
    $.ajax({
        url: "/deleta_dispenser/",
//        dataType: 'json',
        data: {'topico_dispenser': id},
        success: function(){
            location.reload();
        }
    })
}