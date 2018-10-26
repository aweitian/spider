function startInput() {
    var ws = new WebSocket('ws://172.16.6.235:56789/input');
    var initScreenWidth = 360;
    var initScreenHeight = 640;
    var initRotate = 0;//90
    var screen = document.getElementById('screen');
    var ctx = screen.getContext("2d");
    var shouldSendMoveEvent = false;
    ws.onopen = function(event) {
        resizePicture();
    };
    ws.onmessage = function(event) {
        var blob  = new Blob([event.data], {type: "image/jpg"});
        var img = new Image();
        img.onload = function (e) {
            ctx.drawImage(img, 0, 0);
            window.URL.revokeObjectURL(img.src);
            img = null;
        };
        img.onerror = img.onabort = function () {
            img = null;
        };
        img.src = window.URL.createObjectURL(blob);
    };
    ws.onclose = function(event) {
        window.close();
    };
    var down = function(event) {
        shouldSendMoveEvent = true;
        sendFingerPosition("fingerdown", event);
    };
    var up = function(event) {
        sendFingerPosition("fingerup", event)
        shouldSendMoveEvent = false;
    };
    var move = function(event) {
        if (shouldSendMoveEvent) {
            sendFingerPosition("fingermove", event);
        }
    };
    var sendFingerPosition = function(type, event) {
        var x = event.pageX - screen.offsetLeft;
        var y = event.pageY - screen.offsetTop;
        var lastX = x;
        var lastY = y;
        if (initRotate == 90) {
            lastX = y;
            lastY = initScreenWidth - x;
        } else if (initRotate == 180) {
            lastX = initScreenWidth - x;
            lastY = initScreenHeight - y;
        } else if (initRotate == 270) {
            lastX = initScreenHeight - y;
            lastY = x;
        }
        var eventjson = '{"type":"'+type+'","x":'+lastX+',"y":'+lastY+'}';
        ws.send(eventjson);
    };
    var heartbeat = function() {
        ws.send('{"type":"beatheart"}');
    };

    var resizeCanvas = function() {
        screen.width = initScreenWidth;
        screen.height = initScreenHeight;
    };

    var resizePicture = function() {
        if (initScreenWidth <= initScreenHeight) {
            ws.send('{"type":"change_size", "w":'+initScreenWidth+', "h":'+initScreenHeight+', "r":'+ initRotate+'}');
        } else {
            ws.send('{"type":"change_size", "w":'+initScreenHeight+', "h":'+initScreenWidth+', "r":'+ initRotate+'}');
        }
    };

    var buttonHandler = function(e) {
        switch(e.target.id) {
            case "big":
                if (Math.abs(initScreenWidth - initScreenHeight) == 280) {
                    if (initRotate == 90 || initRotate == 270) {
                        initScreenWidth = 1280;
                        initScreenHeight = 720;
                    } else {
                        initScreenWidth = 720;
                        initScreenHeight = 1280;
                    }
                    resizePicture();
                    resizeCanvas();
                }
                break;
            case "small":
                if (Math.abs(initScreenWidth - initScreenHeight) == 560) {
                    if (initRotate == 90 || initRotate == 270) {
                        initScreenWidth = 640;
                        initScreenHeight = 360;
                    } else {
                        initScreenWidth = 360;
                        initScreenHeight = 640;
                    }
                    resizePicture();
                    resizeCanvas();
                }
                break;
            case "rotate":
                if (initRotate == 270) initRotate = 0;
                else initRotate += 90;
                var temp = initScreenHeight;
                initScreenHeight = initScreenWidth;
                initScreenWidth = temp;
                resizePicture();
                resizeCanvas();
                break;
        }
    };
    resizeCanvas();
    screen.addEventListener('mousedown', down, false);
    screen.addEventListener('mouseup', up, false);
    screen.addEventListener('mousemove', move, false);
    document.getElementById('big').addEventListener('click', buttonHandler, false);
    document.getElementById('small').addEventListener('click', buttonHandler, false);
    document.getElementById('rotate').addEventListener('click', buttonHandler, false);
    setInterval("heartbeat()", 2000);
}