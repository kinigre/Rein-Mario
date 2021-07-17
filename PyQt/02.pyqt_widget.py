import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt as qt
from PyQt5.QtWidgets import QApplication,QWidget, QLabel, QPushButton
import numpy as np


class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()

        # 창 크기 조절
        self.setFixedSize(400, 300)
        # 창 제목 설정
        self.setWindowTitle('마리오 학습')

        #버튼
        butten=QPushButton(self)
        butten.setText('버튼')
        butten.setGeometry(200,100,100,100) #(x, y, w, h)

        #텍스트
        lable_text=QLabel(self)
        lable_text.setText('가나다')
        lable_text.setGeometry(200,150,50,100)

        #이미지
        lable_image=QLabel(self)
        image=np.array([[[0,0,0]],[[0,0,0]]])
        q_image=QImage(image, image.shape[1],image.shape[0], QImage.Format_RGB888)
        pixmap=QPixmap(q_image)
        pixmap=pixmap.scaled(100,100, qt.IgnoreAspectRatio)

        lable_image.setPixmap(pixmap)
        lable_image.setGeometry(0,0,100,100)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())