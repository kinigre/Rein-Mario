import sys
import retro
import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class MarioGame(QWidget):
    def __init__(self):
        super().__init__()
        env = retro.make(game="SuperMarioBros-nes", state='Level1-1')
        self.screenSize=int(input(''))
        env.reset()

        #화면 관련
        screen = env.get_screen()# 화면 가져오기
        self.setWindowTitle('마리오 학습')  # 창 제목 설정
        self.setFixedSize(screen.shape[0] * self.screenSize, screen.shape[1] * self.screenSize) # 창 크기 고정
        label_image = QLabel(self)
        self.game_screen(label_image, screen)

        #시간 관련
        self.qTimer=QTimer(self)
        self.qTimer.timeout.connect(self.mario_timer)
        self.qTimer.start(1000)
        #키 배열B, NULL, SELECT, START, U, D, L, R, A
        self.press_buttons = env.step(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
        #화면 출력
        self.show()

    def mario_timer(self):
        self.marioTime-=1
        if self.marioTime==0:
            pass #게임오버가 되도록

    def game_screen(self, label_img, screen):
        image=screen
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(screen.shape[0] * self.screenSize, screen.shape[1] * self.screenSize, Qt.IgnoreAspectRatio)

        label_img.setPixmap(pixmap)
        label_img.setGeometry(0, 0, screen.shape[0] * self.screenSize, screen.shape[1] * self.screenSize)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == event.key_Up:
            self.press_buttons[4] = 0
        elif key == event.key_Down:
            self.press_buttons[5] = 0
        elif key == event.key_Left:
            self.press_buttons[6] = 0
        elif key == event.key_Right:
            self.press_buttons[7] = 0
        elif key == Qt.Key_A:
            self.press_buttons[8] = 0
        elif key == Qt.Key_B:
            self.press_buttons[9] = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarioGame()
    sys.exit(app.exec_())