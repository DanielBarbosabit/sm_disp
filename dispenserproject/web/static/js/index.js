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
//            console.log(dados);
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

//    Atualizacao- grafico temporal
//    console.log(dados.dados)
    var logs_dispenser = dados.dados;
    lista_dados = [];
    var dicionario_ponto = {};

    Object.keys(logs_dispenser).forEach(k =>{
        console.log(k);
        dicionario_ponto['label'] = logs_dispenser[k].data;
        dicionario_ponto['y'] = logs_dispenser[k].papel;

        lista_dados.push(dicionario_ponto);
        dicionario_ponto = {};
    });

    var chart = new CanvasJS.Chart("chartContainer", {
        theme:"light2",
        animationEnabled: false,
        title:{
            text: "Evolução temporal da quantidade de papel"
        },
        axisY :{
            title: "Nível de papel (%)",
            suffix: "%",
            labelAutoFit: false,
            minimum: 0,
            maximum: 100
        },
        toolTip: {
            shared: "true"
        },
        legend:{
            cursor:"pointer",
            itemclick : toggleDataSeries
        },
        data: [{
            type: "line",
            visible: true,
            showInLegend: true,
            yValueFormatString: "##.# %",
            name: "Season 1",
            dataPoints: lista_dados
        }]
    });

chart.render();

function toggleDataSeries(e) {
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
		e.dataSeries.visible = false;
	} else {
		e.dataSeries.visible = true;
	}
	chart.render();
}

}

var lista_dados = [];
window.onload = function () {




}