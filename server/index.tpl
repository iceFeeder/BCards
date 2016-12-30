<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>BCards</title>

    <style>
        li { list-style: none; }
    </style>

    <script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script>
        $(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
                }
            }
            ws = new WebSocket('ws://127.0.0.1:8080/websocket');
            ws.onopen = function(evt) {
                $('#messages').append('<li>Connected to chat.</li>');
            }
            ws.onmessage = function(evt) {
                $('#messages').append('<li>' + evt.data + '</li>');
            }
            $('#send-message').submit(function() {
                ws.send('{"action":"'+$('#action').val()+'",'+'"data":'+$('#data').val()+"}");
                $('#message').val('').focus();
                return false
            });
        });
    </script>
</head>
<body>
    <h2>WebSocket Chat Example</h2>
    <form id="send-message">
        <input id="action" type="text" value="get" />
        <input id="data" type="text" value="1" />
        <input type="submit" value="Send" />
    </form>
    <div id="messages"></div>
</body>
</html>
