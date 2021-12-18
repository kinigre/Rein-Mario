#PPU 스크롤링
import sys
import retro
import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer

class MarioGame(QWidget):
    def __init__(self):
        super().__init__()

        self.env = retro.make(game="SuperMarioBros-nes", state='Level1-1')
        self.env.reset()

        screen_size = int(input('몇배로 출력할건가요?:'))
        self.screen = self.env.get_screen()*screen_size
        self.press_buttons=[0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.setWindowTitle('마리오 학습')
        # 창 크기 고정

        self.screen_width = self.screen.shape[0] * screen_size
        self.screen_height = self.screen.shape[1] * screen_size
        self.setFixedSize(self.screen_width+600 , self.screen_height)

        self.label_image = QLabel(self)
        self.label_image.setGeometry(0, 0, self.screen_width, self.screen_height)

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)
        # 1초(=1000밀리초)마다 연결된 함수를 실행
        qtimer.start(1000 // 60)

        # 창 띄우기
        self.show()

    def timer(self):
        # 키 배열: B, NULL, SELECT, START, U, D, L R, A
        self.env.step(np.array(self.press_buttons))
        self.screen = self.env.get_screen()
        image = self.screen
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        self.label_image.setPixmap(pixmap)
        #페인트 이벤트
        self.update()

    def paintEvent(self, event) :
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)
        ram = self.env.get_ram()

        player_poX, player_poY = self.player_ram(ram)
        enemy_tiles_poX,enemy_tiles_poY =self.enemy_ram(ram)
        screen_tile_offset=self.page_ram(ram)
        full_screen_tiles=self.ram_tiles(ram)
        full_screen_tile_count = full_screen_tiles.shape[0]

        # (13,16)은 16*16의 박스에서 표현되는 타이틀 정보이다.
        full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count // 2].reshape((13, 16))
        full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        # NumPy로 이어붙임 (음수도 잠깐 쓰여서 int64형으로 변환)
        full_screen_tiles=np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)
        screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:,
                                                        screen_tile_offset:screen_tile_offset + 16].astype(np.int)

        #PPU스크롤링
        for i in range(full_screen_tiles.shape[0]):
            for j in range(full_screen_tiles.shape[1]):
                if full_screen_tiles[i][j]==0:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(self.screen_width + 16 * j, 16 * i, 16, 16)
                else:
                    painter.setBrush(QBrush(Qt.cyan))
                    painter.drawRect(self.screen_width + 16 * j, 16 * i, 16, 16)

        #PPU스크롤링 현재 위치
        for n in range(screen_tiles.shape[0]):
            for m in range(screen_tiles.shape[1]):
                if screen_tiles[n][m] == 0:
                    painter.setBrush(QBrush(Qt.gray))
                    painter.drawRect(self.screen_width + 16 * m, self.screen_height//2 + 16 * n, 16, 16)
                else:
                    painter.setBrush(QBrush(Qt.cyan))
                    painter.drawRect(self.screen_width + 16 * m, self.screen_height//2 + 16 * n, 16, 16)

        #플레이어 현재 위치 표시
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(self.screen_width + 16 * player_poX, 16 * player_poY, 16, 16)
        painter.drawRect(self.screen_width + 16 * player_poX,self.screen_height//2 + 16 * player_poY,16,16)

    def ram_tiles(self, ram):
        # 풀 스크린 타일
        full_screen_tiles = ram[0x0500:0x069F + 1]

        return full_screen_tiles

    def page_ram(self, ram):
        current_screen_page = ram[0x071A]
        # 페이지 속 현재 화면 위치
        screen_position = ram[0x071C]
        # 화면 오프셋
        screen_offset = (256 * current_screen_page + screen_position) % 512
        # 타일 화면 오프셋
        screen_tile_offset = screen_offset // 16

        return screen_tile_offset

    def player_ram(self, ram):
        # 현재 화면 속 플레이어 x 좌표
        player_position_x = ram[0x03AD]
        # 0x03B8	Player y pos within current screen
        # 현재 화면 속 플레이어 y 좌표
        player_position_y = ram[0x03B8]
        # 타일 좌표로 변환
        player_tile_position_x = (player_position_x + 8) // 16
        player_tile_position_y = (player_position_y + 8) // 16 - 1

        return player_tile_position_x, player_tile_position_y

    def enemy_ram(self, ram):
        # 자신이 속한 화면 페이지 번호
        enemy_horizon_position = ram[0x006E:0x0072 + 1]
        # 0x0087-0x008B	Enemy x position on screen
        # 자신이 속한 페이지 속 x 좌표
        enemy_screen_position_x = ram[0x0087:0x008B + 1]
        # 0x00CF-0x00D3	Enemy y pos on screen
        enemy_position_y = ram[0x00CF:0x00D3 + 1]
        # 적 x 좌표
        enemy_position_x = (enemy_horizon_position * 256 + enemy_screen_position_x) % 512
        # 적 타일 좌표
        enemy_tile_position_x = (enemy_position_x + 8) // 16
        enemy_tile_position_y = (enemy_position_y - 8) // 16 - 1

        return enemy_tile_position_x, enemy_tile_position_y

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_S:
            self.press_buttons[0] = 1
        elif key == Qt.Key_Up:
            self.press_buttons[4] = 1
        elif key == Qt.Key_Down:
            self.press_buttons[5] = 1
        elif key == Qt.Key_Left:
            self.press_buttons[6] = 1
        elif key == Qt.Key_Right:
            self.press_buttons[7] = 1
        elif key == Qt.Key_A:
            self.press_buttons[8] = 1
        if key == Qt.Key_R:
            self.env.reset()

    # 키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_S:
            self.press_buttons[0] = 0
        elif key == Qt.Key_Up:
            self.press_buttons[4] = 0
        elif key == Qt.Key_Down:
            self.press_buttons[5] = 0
        elif key == Qt.Key_Left:
            self.press_buttons[6] = 0
        elif key == Qt.Key_Right:
            self.press_buttons[7] = 0
        elif key == Qt.Key_A:
            self.press_buttons[8] = 0

    def closeEvent(self, event):
        self.deleteLater()

#소리까지 env.em.get_오디오
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarioGame()
    sys.exit(app.exec_())