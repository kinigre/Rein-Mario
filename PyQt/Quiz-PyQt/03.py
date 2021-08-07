'''
[도전과제2]
[사각형 가이드]
사각형 크기 (50 x 50)
사각형 색 (파랑, 없음, 없음, 빨강)

[그래프 가이드]
원 반지름 (25)
원 색상 윗층 - (청록, 흰색, 청록) , 아랫층 - (회색)
선 색상 (빨강, 파랑, 빨강)
선을 먼저 그리고, 원 그리기
원 중심 좌표 = 왼쪽 위 좌표 + 반지름
'''

import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt as qt
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 조절
        self.setFixedSize(200, 300)  # 1024 x 768
        # 창 제목 설정
        self.setWindowTitle('GA-lab_Mario')
        # 창 띄우기
        self.show()

    # 창이 업데이트 할때 마다 실행되는 함수
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        #1사각형
        painter.setBrush(QBrush(qt.blue))
        painter.drawRect(0, 0, 50, 50)
        painter.setBrush(qt.NoBrush)
        painter.drawRect(0, 51, 50, 50)
        painter.drawRect(51, 0, 50, 50)
        painter.setBrush(QBrush(qt.red))
        painter.drawRect(51, 51, 50, 50)
        painter.setBrush(qt.NoBrush)
        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))

        #2뉴런
        painter.setPen(QPen(qt.red, 2.0, qt.SolidLine))
        painter.drawLine(25,175,75,275)
        painter.setPen(QPen(qt.blue, 2.0, qt.SolidLine))
        painter.drawLine(75, 175, 75, 275)
        painter.setPen(QPen(qt.red, 2.0, qt.SolidLine))
        painter.drawLine(125 ,175, 75, 275)

        painter.setPen(QPen(qt.black, 1.0, qt.SolidLine))
        painter.setBrush(QBrush(qt.cyan))
        painter.drawEllipse(0, 150, 50, 50)
        painter.setBrush(qt.NoBrush)
        painter.setBrush(QBrush(qt.white))
        painter.drawEllipse(50, 150, 50, 50)
        painter.setBrush(qt.NoBrush)
        painter.setBrush(QBrush(qt.cyan))
        painter.drawEllipse(100, 150, 50, 50)
        painter.setBrush(qt.NoBrush)
        painter.setBrush(QBrush(qt.gray))
        painter.drawEllipse(50, 250, 50, 50)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())