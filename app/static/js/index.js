$(document).ready(function(){
    const socket = io.connect('http://127.0.0.1:5000');

    socket.emit('room_request')

    socket.on('room_update', function(rooms){

        for (let i = 0; i < rooms.length; i += 3){
            room_group = document.createElement('div')
            room_group.setAttribute('class', 'room_box_group')

            for (let j = i; j < i + 3 && j < rooms.length; j++){
                room = rooms[j]

                room_div = document.createElement('div')
                room_div.setAttribute('class', 'room_box_data')

                room_name = document.createElement('h1')
                room_name.setAttribute('class', 'center')
                room_name.setAttribute('style', 'font-size:40px; margin:0')
                room_name.appendChild(document.createTextNode(room['name']))

                users_list = document.createElement('b')
                //users_list.setAttribute()
                users_list_text = ''

                for (let k = 0; k < room['users'].length; k++){
                    user = room['users'][k]

                    users_list_text += user.username

                }


                room_div.appendChild(room_name)

                room_group.appendChild(room_div)
            }
            document.getElementById('room_list').appendChild(room_group)
        }
    });
});