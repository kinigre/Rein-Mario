import retro
env=retro.make(game="SuperMarioBros-nes", state='Level1-1')
env.reset()

print(env)
# env.get_ram() #게임에서 램에 정보를 가져온다.