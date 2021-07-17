#03. get_screen.py 에서 가져온 화면 정보를 pyqt QLabel에 띄우기
from PyQt5.QtWidgets import QLabel,QApplication,QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt as qt
import retro
import sys
import numpy as np

class GameScreen(QWidget):
    def __init__(self):
        super(GameScreen,self).__init__()
        self.setFixedSize(300, 300)
        self.setWindowTitle('마리오 학습')

        # 게임 환경 생성
        env = retro.make(game="SuperMarioBros-nes", state='Level1-1')
        # 새 게임 시작
        env.reset()
        # 화면 가져오기
        screen = env.get_screen()
        label_img=QLabel(self)
        img=np.array([[[screen.shape[0]]], [[screen.shape[1]]]])
        q_image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(q_image)
        pixmap = pixmap.scaled(100, 100, qt.IgnoreAspectRatio)

        label_img.setPixmap(pixmap)
        label_img.setGeometry(0, 0, 100, 100)
        self.show()

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = GameScreen()
    sys.exit(app.exec_())
#추가 과제: 화면 해상도를 2배 키워서 띄우기 (pixmap scaled 활용)