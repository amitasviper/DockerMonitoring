function get_data(){
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.emit('channel_container_ids_req', 'ready');

    socket.on('channel_container_ids_resp', function (data) {
        show('page', true);
        show('loading', false);
        //console.log(data);
        //var json = JSON.parse($.trim(data));
        console.log('Got container_id : ' + data);

        $.each(data, function (index, value) {
          console.log(value.Command + " " + value.Names[0] + " " + value.Id + " " + value.Status);
          $('#table_containers').append('<tr><td>' + value.Command + '</td><td>' + value.Names[0] + '</td><td id = "id" onclick="container_info(\'' + value.Id + '\')"><a>' + value.Id + '</a></td><td>' + value.Status + '</td><td>' + value.Image + '</td><td>' + value.Created + '</td></tr>');
          $('#id').mouseover(function () {
            console.log("Mouse Over");
          })
        });
    });
}

function container_info(id) {
    window.location.href = '/container/' + id;
}

function initialise(){
	show('page', false);
  show('loading', true);
	get_data();
}

function show(id, value) {
    document.getElementById(id).style.display = value ? 'block' : 'none';
}

$(document).ready(initialise);