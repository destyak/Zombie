# 1 - Menginstall pygame
import pygame
from pygame.locals import *
import math
from random import randint

# 2 - Menentukan ukuran layar game
pygame.init()
width, height = 640, 480
pygame.display.set_caption("Zombie")
screen = pygame.display.set_mode((width, height))

# Key mapping
keys = {
    "top": False, 
    "bottom": False,
    "left": False,
    "right": False 
}
running = True

playerpos = [100, 100] # x, y peletakkan pemain

# exit code for game over and win codition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1

score = 0 
health_point = 194 # default health point for castle
countdown_timer = 90000 # 90 detik
arrows = [] # list of arrows

enemy_timer = 100 # waktu kemunculan
enemies = [[width, 100]] # list yang menampung koordinat musuh

# 3 - Asset game
# 3.1 - Gambar
player = pygame.image.load("resources/img/ninja.png")
soil = pygame.image.load("resources/img/soil.png")
castle = pygame.image.load("resources/img/castle.png")
arrow = pygame.image.load("resources/img/kunai.png")
enemy_img = pygame.image.load("resources/img/zombie.png")
healthbar = pygame.image.load("resources/img/healthbar.png")
health = pygame.image.load("resources/img/health.png")
gameover = pygame.image.load("resources/img/gameover.png")
youwin = pygame.image.load("resources/img/youwin.png")

# 3.1 - Suara
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.2)
enemy_hit_sound.set_volume(0.2)
shoot_sound.set_volume(0.2)

# background music
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.1)

## 4 - Game Loop
while(running):
    
    # 5 - Clear screen
    screen.fill(0)
    
    # 6 - Draw the game object
    
    # draw the soil
    for x in range(int(width/soil.get_width()+1)):
        for y in range(int(height/soil.get_height()+1)):
            screen.blit(soil, (x*100, y*100))
	
	# draw the castle
    screen.blit(castle, (0, 30)) #(tuple x,y castle)
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # draw the player
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
    new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)

    # 6.1 - Draw arrows
    for kunai in arrows:
        arrow_index = 0
        velx=math.cos(kunai[0])*8
        vely=math.sin(kunai[0])*8
        kunai[1]+=velx
        kunai[2]+=vely
        if kunai[1] < -46 or kunai[1] > width or kunai[2] < -46 or kunai[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        # draw the arrow
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

   # 6.2 - Draw Enemy
    # waktu musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        # buat musuh baru
        enemies.append([width, randint(50, height-32)])
        # reset enemy timer to random time
        enemy_timer = randint(1, 400)

    index = 0
    for enemy in enemies:
        # musuh bergerak dengan kecepatan 5 pixel ke kiri
        enemy[0] -= 1
        # hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -46:
            enemies.pop(index)
            
      # 6.2.1 collision between enemies and castle 
        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y 
        enemy_rect.left = enemy[0] # ambil titik x
        # benturan musuh dengan markas
        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint(5,20)
            hit_sound.play()
            print("Gawat, zombie menyerang!!")
        
        # 6.2.2 Check for collisions between enemies and arrows
        index_arrow = 0
        for kunai in arrows:
            kunai_rect = pygame.Rect(arrow.get_rect())
            kunai_rect.left = kunai[1]
            kunai_rect.top = kunai[2]
            # benturan anak panah dengan musuh
            if enemy_rect.colliderect(kunai_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)
                enemy_hit_sound.play()
                print("Yay, KENA!")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1

    # gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    # 6.3 - Draw Health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)
    
    # 7 - Update the sceeen
    pygame.display.flip()

    # 8 - Event Loop
    for event in pygame.event.get():
        
        # event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            
        # Fire!!
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
            shoot_sound.play()
        
        # tombol untuk naik turun
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False
                
    # - End of event loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 9. Agar pemain bisa pindah
    if keys["top"]:
        playerpos[1] -= 3 # kurangi nilai y
    elif keys["bottom"]:
        playerpos[1] += 3 # tambah nilai y 
    if keys["left"]:
        playerpos[0] -= 3 # kurangi nilai x
    elif keys["right"]:
        playerpos[0] += 3 # tambah nilai x

    # 10 - Cek Menang/Kalah
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

# - End of Game Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# 11 - Menampilkan hasil akhir win/lose
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))

# Tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()