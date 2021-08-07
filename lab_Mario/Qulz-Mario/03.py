#03. get_screen.py 에서 가져온 화면 정보를 pyqt QLabel에 띄우기
from PyQt5.QtWidgets import QLabel,QApplication,QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt as qt
import retro
import sys

class GameScreen(QWidget):
    def __init__(self):
        super(GameScreen,self).__init__()
        # 게임 환경 생성
        env = retro.make(game="SuperMarioBros-nes", state='Level1-1')
        # 새 게임 시작
        env.reset()
        # 화면 가져오기
        screen = env.get_screen()
        screenSize=int(input('몇배 키우실건가요?:'))
        # 창 크기 고정
        self.setFixedSize(screen.shape[0]*screenSize, screen.shape[1]*screenSize)
        # 창 제목 설정
        self.setWindowTitle('마리오 학습')

        label_image = QLabel(self)
        image = screen
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(screen.shape[0]*screenSize, screen.shape[1]*screenSize, qt.IgnoreAspectRatio)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0,0, screen.shape[0]*screenSize, screen.shape[1]*screenSize)

        # 창 띄우기
        self.show()


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = GameScreen()
    sys.exit(app.exec_())
#추가 과제: 화면 해상도를 2배 키워서 띄우기 (pixmap scaled 활용)