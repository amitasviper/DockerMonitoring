function get_dummy_data(div1, div2, div3){
	$.ajax({
  		type: 'GET',
  		url: url,
  		dataType: 'json',
		success: function(data){
			$(div1).text(data['cpu_usage']);
		}
	});
}