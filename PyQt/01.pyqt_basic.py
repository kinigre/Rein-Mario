from PyQt5.QtWidgets import QApplication , QWidget
import sys

class MyApp(QWidget):

    def __init__(self):
        super(MyApp, self).__init__()
        
        #창 크기 조절
        self.setFixedSize(400,300)
        #창 제목 설정
        self.setWindowTitle('마리오 학습')
        #창 띄우기
        self.show()

if __name__ =='__main__':
    app=QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())