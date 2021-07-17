from PyQt5.QtWidgets import QApplication, QWidget
import sys
from PyQt5.QtCore import QTimer

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()

        # 창 크기 조절
        self.setFixedSize(400, 300)
        # 창 제목 설정
        self.setWindowTitle('마리오 학습')

        #타이머 생성
        qtimer=QTimer(self)
        #타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)
        #1초마다 연결된 함수를 실행
        qtimer.start(1000) #1초

        # 창 띄우기
        self.show()

    def timer(self):
        pass
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())