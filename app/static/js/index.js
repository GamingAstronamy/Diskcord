$(document).ready(function(){
    const socket = io.connect('http://127.0.0.1:5000');

    socket.emit('room_request')

    socket.on('room_update', function(rooms){

        for (let i = 0; i < rooms.length * 10; i ++) {
            let room = rooms[0]
            
            room_entry = document.createElement('div')
            room_entry.setAttribute('class', 'room_entry')

            room_image = document.createElement('img')
            room_image.setAttribute('src', room['image_url'])
            room_image.setAttribute('class', 'room_entry_image')

            room_name = document.createElement('h2')
            room_name.setAttribute('class', 'room_entry_name')
            room_name.appendChild(document.createTextNode(room['name']))

            room_users = document.createElement('h3')
            room_users.setAttribute('class', 'room_entry_users')
            let room_users_text = ''
            for (let j = 0; j < room['users'].length; j ++){
                user = room['users'][j]
            }

            room_entry.appendChild(room_image)
            room_entry.appendChild(room_name)

            document.getElementById('room_list').appendChild(room_entry)
        }

    });
});