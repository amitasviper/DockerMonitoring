
var memory_series, cpu_series, network_series;

function get_data(var_series, var_url, json_key){
    //console.log("calling for : " + json_key);
	$.ajax({
  		type: 'GET',
  		//async: false,
  		url: var_url,
  		dataType: 'json',
		success: function(data){
            show('page', true);
            show('loading', false);

			x = (new Date()).getTime(); // current time
			if(json_key == 'cpu_usage'){
                //console.log("The cpu_usage array is : " + JSON.stringify(data));
                var flag = false;
                var flag2 = false;
                for(i = 0; i < var_series.length; i++){
                    if(i == var_series.length - 1){
                        flag = true;
                        flag2 = true;
                    }
                    z = data.cpu_usage[i];
                    var_series[i].addPoint([x, z], flag, flag2);
                }
			}
            else{
                y = data[json_key];
                console.log("The x and y values are : " + x + "  "+ y);
                var_series[0].addPoint([x, y], true, true);
            }
            
			//console.log("Series : "+var_series[0])
			get_data(var_series, var_url, json_key);
		},
		error: function(status, error){
			x = (new Date()).getTime(); // current time
			y = 0;
			if(json_key == 'cpu_usage'){
				var_series[1].addPoint([x, Math.random()], true, true);

			}
			var_series[0].addPoint([x, y], true, true);
			console.log("Into error");
			setTimeout(function(){get_data(var_series, var_url, json_key)}, 2000);
		}
	});
}

function initialise(){
	console.log("Into the initialise phase");
	render_chart("#memory_usage_chart", memory_series, '/jsondata', 'memory_usage');
	render_chart("#cpu_usage_chart", cpu_series, '/jsondata', 'cpu_usage');
	render_chart("#network_usage_chart", network_series, '/jsondata', 'network_usage');

}

function render_chart(container_name, series_name, url, json_key) {
    $(document).ready(function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $(container_name).highcharts({
            chart: {
                type: 'spline',
                animation: true, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        series_name = this.series;
                        console.log("Size of the series is : " + series_name.length);
                        get_data(series_name, url, json_key);
                    }
                }
            },
            title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: create_series_array(json_key)
        });
    });
}

function create_series_array(json_key){
	var size = 1;
	if (json_key == 'cpu_usage') {

		size = 2;
        $.ajax({
        type: 'GET',
        async: false,
        url: '/jsondata',
        dataType: 'json',
        success: function(data){
            //data = JSON.parse(data);
            console.log("The type is : " + data.cpu_usage.length);
            size = data.cpu_usage.length;
        },
        error: function(status, error){
            size = 1;
        }
    });

	};
	var temp_series = [];
	for (j = 0; j <size; j += 1){
		instance_series = {
			name: 'Random data',
			data: (function () {
			    	// generate an array of random data
			    	var data = [],
			    	    time = (new Date()).getTime(),
			    	    i;
			
			    	for (i = -19; i <= 0; i += 1) {
			    	    data.push({
			    	        x: time + i * 1000,
			    	        y: Math.random()
			    	    });
			    	}
			    	return data;
			    }())
			}
		temp_series[j] = instance_series;
	}
	return temp_series;
}

function show(id, value) {
    document.getElementById(id).style.display = value ? 'block' : 'none';
}

$(document).ready(initialise);