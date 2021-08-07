import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel
from PyQt5.QtCore import QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 고정
        self.setFixedSize(400, 300)
        # 창 제목 설정
        self.setWindowTitle('MyApp')
        self.cnt=0
        # 타이머 생성
        self.qtimer = QTimer(self)
        # 타이머에 호출할 함수 연결
        self.qtimer.timeout.connect(self.timerCnt)
        # 1초(=1000밀리초)마다 연결된 함수를 실행
        self.qtimer.start(1000)
        self.label = QLabel(self)
        self.label.setGeometry(200, 200, 50, 100)  # 크기, 위치 합쳐놓은것

        # 창 띄우기
        self.show()


    def timerCnt(self):
        self.cnt+=1
        self.label.setText(str(self.cnt) + '초')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())