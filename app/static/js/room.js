$(document).ready(function() {
    const socket = io.connect('https://www.diskcord.ga')

    socket.emit('message_request')

    socket.on('message_database_change', function(messages){

        maxScrollDown = document.getElementById('messages').scrollHeight -  document.getElementById('messages').clientHeight;

        render_messages(messages)

        let new_maxScrollDown = document.getElementById('messages').scrollHeight -  document.getElementById('messages').clientHeight;

        if (maxScrollDown != new_maxScrollDown && maxScrollDown - $('#messages').scrollTop() < 25){
            $('#messages').scrollTop(new_maxScrollDown)
            maxScrollDown = new_maxScrollDown;
        }
    });

    function render_messages(messages){

        $('#messages').html('')

        for (let i = 0; i < messages.length; i++) {
            var message = messages[i]
            console.log(message)

            div = document.createElement('div');
            div.setAttribute('class','message')

            para = document.createElement('p');
            para.setAttribute('class','white');

            bold1 = document.createElement('b');
            bold1.setAttribute('style', 'color:' + message['author']['color'] + '; letter-spacing: 1px');

            bold2 = document.createElement('b');
            bold2.setAttribute('style', 'margin: 1px; font-size:10px; color:#585e66');

            node1 = document.createTextNode(message['author']['nickname'] + '  ');
            node2 = document.createTextNode(message['timestamp']);
            node3 = document.createTextNode(message['content']);

            bold1.appendChild(node1);
            bold2.appendChild(node2);

            para.appendChild(bold1);
            para.appendChild(bold2);
            para.appendChild(document.createElement('br'))
            para.appendChild(node3);

            div.appendChild(para);

            document.getElementById('messages').appendChild(div);
        }

    }

    $('#message_box').keyup(function(event){
        var text = $(this).val();

        if (event.key === 'Enter' && text != ''){
            
            socket.emit('new_message', text)

            $('#message_box').val('');
        }
    });

});