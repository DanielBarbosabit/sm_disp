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

    if(dados.dispenser != 0){
        $('#sem_dispenser').hide();

        var logs = dados.dispenser;
        var dicionario_ponto = {};
        var dados_dispenser;
        lista_dados = [];
        var lista_graficos = [];
        var dicts_dispenser = {};

    //    Variaveis do grafico de bateria
        var dicionario_ponto_bateria = {};
        var lista_dados_bateria = [];
        var dicts_dispenser_bateria = {};
        var lista_graficos_baterias = [];

        Object.keys(logs).forEach(k =>{
            console.log(logs[k]);
            dados_dispenser = logs[k].dados;
            Object.keys(dados_dispenser).forEach(i =>{

    //                Dicionario do gráfico de consumo
                    dicionario_ponto['label'] = dados_dispenser[i].data;
                    dicionario_ponto['y'] = dados_dispenser[i].papel;

    //                Dicionario do grafico de tensão de bateria
                    dicionario_ponto_bateria['label'] = dados_dispenser[i].data;
                    dicionario_ponto_bateria['y'] = dados_dispenser[i].bateria;

    //                Inclusao de pontos do grafico de consumo
                    lista_dados.push(dicionario_ponto);
                    dicionario_ponto = {};

    //                Inclusao de pontos do grafico de tensao
                    lista_dados_bateria.push(dicionario_ponto_bateria);
                    dicionario_ponto_bateria = {};

            })
    //        Inclusao de uma linha para cada dispenser

            dicts_dispenser['type'] = "line";
            dicts_dispenser['visible'] = true;
            dicts_dispenser['showInLegend'] = true;
            dicts_dispenser['yValueFormatString'] = "##.#%" / 100,
            dicts_dispenser['name'] = logs[k].topico;
            dicts_dispenser['dataPoints'] = lista_dados;
            lista_dados = [];

            lista_graficos.push(dicts_dispenser);
            dicts_dispenser = {};

            dicts_dispenser_bateria['type'] = "line";
            dicts_dispenser_bateria['visible'] = true;
            dicts_dispenser_bateria['showInLegend'] = true;
            dicts_dispenser_bateria['yValueFormatString'] = "#.## V",
            dicts_dispenser_bateria['name'] = logs[k].topico;
            dicts_dispenser_bateria['dataPoints'] = lista_dados_bateria;
            lista_dados_bateria = [];

            lista_graficos_baterias.push(dicts_dispenser_bateria);
            dicts_dispenser_bateria = {};
        })

        inicializacao = 1;

        var chart = new CanvasJS.Chart("chartContainer", {
            theme:"light3",
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
            data: lista_graficos
        });

        var chart_bateria = new CanvasJS.Chart("grafico_bateria", {
            theme:"light3",
            animationEnabled: false,
            title:{
                text: "Tensão das baterias"
            },
            axisY :{
                title: "Tensão (V)",
                suffix: "V",
                labelAutoFit: false,
                minimum: 0,
                maximum: 7
            },
            toolTip: {
                shared: "true"
            },
            legend:{
                cursor:"pointer",
                itemclick : toggleDataSeries
            },
            data: lista_graficos_baterias
        });

        chart.render();
        chart_bateria.render();

        function toggleDataSeries(e) {
            if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
                e.dataSeries.visible = false;
            } else {
                e.dataSeries.visible = true;
            }
            chart.render();
            chart_bateria.render();
        }
    }else{
        $('#sem_dispenser').show();
        $('#chartContainer').hide();
        $('#grafico_bateria').hide();
    }
}
