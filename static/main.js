/**
 * Created by tito on 06.08.17.
 */
function Ready() {
    $(document).ready(function () {
            function ReturnData() {
        var response = $.ajax({
            url: '/get_data',
            async: false,
            dataType: "json",
//                success: function (data) {
//                    return data;
//
//            }
        }).responseText;
        var data = $.parseJSON(response);
                console.log(response);
        return data
    }
    var a = ReturnData();
Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        type:'category',
        title: {
            text: ''
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="font-size:11px; color:{point.color} ">{point.name}</span>: <b>{point.y}</b> of total<br/>'
    },

    series: [{
        name: 'Countries',
        colorByPoint: true,
        data: a.series_data
    }],
    drilldown: {
        series: a.dril_data
    }
});
});
}
