$(document).ready(function() {
    atualiza_grafico_pizza();
});


function atualiza_grafico_pizza(){
    //função para atualizar o chart

    setInterval(function(){
        console.log('realizando atualizacao do grafico...')
        $.ajax({
          dataType: 'json',
          url: '/busca_dados_atuais/',
//          data: data,
          success: function(dados){
            console.log(dados);
            grafico_pizza(dados)
          }
        });
    },2000);

}

function grafico_pizza(dados){
    var porcentagem_final;
    porcentagem_final = dados.paper_level;
    if (porcentagem_final == '0Z')
        porcentagem_final = 0;
    if (porcentagem_final == '0C')
        porcentagem_final = 100;
    pieChart.data.datasets[0].data[0] = 100 - porcentagem_final;
    pieChart.data.datasets[0].data[1] = porcentagem_final;
    pieChart.update();
}