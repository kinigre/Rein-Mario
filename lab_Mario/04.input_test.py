import retro
import numpy as np

#게임 환경 생성
env=retro.make(game="SuperMarioBros-nes", state='Level1-1')

#새 게임 시작
env.reset()

#키 배열: B, NULL, SELECT, START, U, D, L, R, A
env.step(np.array([0,0,0,0,0,0,1,0]))