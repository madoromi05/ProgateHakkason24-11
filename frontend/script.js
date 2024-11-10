document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector("img.rokuonnB");  // 録音ボタン
    const recordingStatus = document.getElementById("recordingStatus");
    let mediaRecorder;
    let socket;
    let audioStream = null;  // マイクのストリームを保持
    const websocketURL = "";  // WebSocketのURL。必要であれば設定

    // 初回のみマイクのアクセス許可を確認
    async function initMicrophone() {
        try {
            audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log("マイクのアクセスが許可されました");
        } catch (error) {
            console.error("マイクへのアクセスが拒否されました:", error);
        }
    }

    // WebSocket接続を開始
    function startWebSocket() {
        if (websocketURL) {
            socket = new WebSocket(websocketURL);

            socket.onopen = function() {
                console.log("WebSocket接続が開かれました");
            };

            socket.onerror = function(error) {
                console.error("WebSocketエラー:", error);
            };

            socket.onclose = function() {
                console.log("WebSocket接続が閉じられました");
            };
        } else {
            console.warn("WebSocket URLが設定されていないため、データは送信されません。");
        }
    }

    // 録音の開始処理
    function startRecording() {
        if (audioStream) {
            mediaRecorder = new MediaRecorder(audioStream);

            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0 && socket && socket.readyState === WebSocket.OPEN) {
                    socket.send(event.data);  // WebSocketが開いている場合のみ送信
                }
            };

            mediaRecorder.start();
            recordingStatus.style.display = "block";  // 録音中の表示
        } else {
            console.error("マイクが初期化されていないため、録音を開始できません。");
        }
    }

    // 録音の停止処理
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
        }
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
        recordingStatus.style.display = "none";  // 録音中の表示をOFF
    }

    // ページ読み込み時にマイクの初期化を行う
    initMicrophone();

    // 録音ボタンにイベントリスナーを設定
    button.addEventListener("mousedown", function() {
        startWebSocket();
        startRecording();
    });

    button.addEventListener("mouseup", stopRecording);
    button.addEventListener("touchstart", function() {
        startWebSocket();
        startRecording();
    });

    button.addEventListener("touchend", stopRecording);
});
