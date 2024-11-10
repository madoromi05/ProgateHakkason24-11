document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector("img.rokuonnB");
    const recordingStatus = document.getElementById("recordingStatus");

    // ボタンが押された時に「録音中」を表示
    function showRecording() {
        recordingStatus.style.display = "block";
    }

    // ボタンが離された時に「録音中」を非表示
    function hideRecording() {
        recordingStatus.style.display = "none";
    }

    // マウスとタッチイベントの両方に対応
    button.addEventListener("mousedown", showRecording);
    button.addEventListener("mouseup", hideRecording);
    button.addEventListener("touchstart", showRecording);
    button.addEventListener("touchend", hideRecording);
});