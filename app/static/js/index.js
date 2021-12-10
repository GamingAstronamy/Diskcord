$(document).ready(function(){
    const socket = io.connect('https://www.diskcord.ga');

    socket.emit('room_request')

    socket.on('room_update', function(rooms){

        for (let i = 0; i < rooms.length; i ++) {
            let room = rooms[i]
            
            room_entry = document.createElement('div')
            room_entry.setAttribute('class', 'room_entry unselectable')
            room_entry.setAttribute('roomid', room['id'])

            console.log(room_entry.getAttribute('roomid'))

            room_data = document.createElement('div')
            room_data.setAttribute('class', 'room_data')
            
            room_image = document.createElement('img')
            room_image.setAttribute('class', 'room_entry_image')
            if (UrlExists(room['image_url'])) {
                room_image.setAttribute('src', room['image_url'])
            } else {
                room_image.setAttribute('src', 'static/photos/DiskcordGrey.svg')
            }

            room_name = document.createElement('h2')
            room_name.setAttribute('class', 'room_entry_name')
            room_name.appendChild(document.createTextNode(room['name']))

            room_users = document.createElement('h3')
            room_users.setAttribute('class', 'room_entry_users')
            var room_users_text = ''
            for (let j = 0; j < room['users'].length; j ++){
                user = room['users'][j]
                room_users_text += user['username'] + ' '
            }
            room_users.appendChild(document.createTextNode('Users: ' + room_users_text))

            room_data.appendChild(room_name)
            room_data.appendChild(room_users)

            room_entry.appendChild(room_image)
            room_entry.appendChild(room_data)

            document.getElementById('room_list').appendChild(room_entry)
        }

        $('div.room_entry').hover(function(){

            $(this).removeClass('room_entry').addClass('room_entry_hover')
    
        }, function(){

            $(this).removeClass('room_entry_hover').addClass('room_entry')
            
        });

        $('div.room_entry').click(function(){

            room_id = $(this).attr('roomid')

            socket.emit('room_change_request', room_id)

            window.location.href = "https://www.diskcord.ga/room";

        });

        function UrlExists(url){
            var http = new XMLHttpRequest();
            http.open('HEAD', url, false);
            http.send();
            return http.status!=404;
        }

    });

    
});