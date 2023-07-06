import sys
import os
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
import numpy as np
from PIL import Image

def get_resized_pixel_data(pixel_data, original_width, original_height):
    array_data = np.array(pixel_data, dtype=np.uint8).reshape((original_height, original_width, 4))
    
    image = Image.fromarray(array_data, mode='RGBA')
    grayscale_image = image.convert('L')
    resized_image = grayscale_image.resize((28, 28), Image.ANTIALIAS)
    
    resized_pixel_data = np.array(resized_image).reshape(-1).tolist()

    return resized_pixel_data

class Backend(QObject):
    number_guessed = pyqtSignal(str)
    
    @pyqtSlot(list, int, int)
    def Guess_number(self, pixels: list, width, height):
        resized_pixels = get_resized_pixel_data(pixels, width, height)
        print(len(pixels))
        print(len(resized_pixels))
        pass

qmlRegisterType(Backend, "Backend", 1, 0, "Backend")
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))
sys.exit(app.exec())