import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQml 2.15
import Backend 1.0

ApplicationWindow{
    visible: true
    width: 400
    color: "#0e1117"
    Material.accent: "#e91e63"
    height: 400
    title: "DrawingApp"

    Backend{
        id: backend
        onNumber_guessed: numberString => numberTitle.Text = numberString;
    }

    Text{
        id: numberTitle
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 24
        color: "white"
        text: "hello"
    }

    Canvas{
        id: canvas
        anchors.fill: parent
        property real prevX: -1
        property real prevY: -1

        function getPixelData(){
            var ctx = getContext("2d");
            var pixelData = ctx.getImageData(0, 0, width, height);
            var pixelDataList = Array.from(pixelData.data);
            return pixelDataList;
        }

        function clearCanvas() {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            requestPaint()
        }

        onPaint: {
            var ctx = getContext("2d");
            ctx.lineWidth = 3;
            ctx.strokeStyle = "white"
            ctx.beginPath();
            if (prevX >= 0 && prevY >= 0) {
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(mouseArea.mouseX, mouseArea.mouseY);
            }
            ctx.stroke();
            prevX = mouseArea.mouseX;
            prevY = mouseArea.mouseY;
        }
    }

    MouseArea{
        id: mouseArea
        anchors.fill: parent
        onPressed: {
            canvas.prevX = mouseX;
            canvas.prevY = mouseY;
            canvas.requestPaint();
        }
        onPositionChanged: canvas.requestPaint()
        onReleased: {
            canvas.prevX = -1;
            canvas.prevY = -1;
            backend.Guess_number(canvas.getPixelData(), canvas.width, canvas.height)
        }
    }

    Button{
        text: "Clear"
        onClicked: canvas.clearCanvas();
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
}