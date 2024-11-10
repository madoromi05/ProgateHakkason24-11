// script.js
document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector(".modoru");
    const recordingStatus = document.getElementById("recordingStatus");

    // ボタンが押された時に「録音中」を表示
    button.addEventListener("mousedown", function() {
        recordingStatus.style.display = "block";
    });

    // ボタンが離された時に「録音中」を非表示
    button.addEventListener("mouseup", function() {
        recordingStatus.style.display = "none";
    });

    // タッチ対応 (モバイルデバイス用)
    button.addEventListener("touchstart", function() {
        recordingStatus.style.display = "block";
    });

    button.addEventListener("touchend", function() {
        recordingStatus.style.display = "none";
    });
});