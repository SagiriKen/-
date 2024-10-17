import pygame
import random
import os
FPS = 60
WIDTH = 500
HEIGHT = 600
score = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("宇宙大戰") #遊戲名子
clock = pygame.time.Clock()
#載入圖片
background_img = pygame.image.load(os.path.join("123",'background.jpeg')).convert()
player_img = pygame.image.load((os.path.join("123","player.png"))).convert()


player_mini_img = pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
rock_img = pygame.image.load((os.path.join("123","rock.png"))).convert()
bullet_img = pygame.image.load((os.path.join("123","bullet.png"))).convert()
pygame.display.set_icon((player_mini_img)) #左上角圖片
"""
expl_anim = {}
expl_anim["lg"]=[]
expl_anim["sm"]=[]
for i in range(9):
    expl_img = pygame.image.load(os.path.join(f"C:/Users/童冠翔/Desktop/PYTHON/expl{i}.png"))
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (30, 30)))
"""
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("123","shield.png"))
power_imgs['gun'] = pygame.image.load(os.path.join("123","gun.png"))

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("123","shoot.wav"))
pygame.mixer.music.load(os.path.join("123","background.ogg"))
pygame.mixer.music.set_volume(0.2)
font_name = os.path.join("123","123.ttf")
def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)
def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img,img_rect)
def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen,'宇宙大戰',64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"左右鍵移動飛船  空白艦發射子彈",22,WIDTH/2,HEIGHT/2)
    draw_text(screen,"按任意鍵開始遊戲",18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.center = ((WIDTH/2,HEIGHT-30))
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -=1
            self.gun_time = now
        if self.hidden and pygame.time.get_ticks() - self.hide_time>1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 10)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right >WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add((bullet))
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.y)
                bullet2 = Bullet(self.rect.right, self.rect.y)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add((bullet1))
                bullets.add((bullet2))
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2,HEIGHT+500)
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = ((random.randrange(0,WIDTH - self.rect.width),random.randrange(-100,-40)))
        self.speedy = random.randrange(3,10)  #隕石速度
        self.speedx = random.randrange(-3, 3)


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right < 0:
            self.rect.center = ((random.randrange(0, WIDTH - self.rect.width), random.randrange(-100, -40)))
            self.speedy = random.randrange(3, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()
"""
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect
                self.rect.center = center
"""

pygame.mixer.music.play(-1)

show_init = True
running= True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
    clock.tick(FPS)
    #輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #按鍵盤
            if event.key == pygame.K_SPACE:
                player.shoot()
    #更新
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        score += 20#hit.radius
        #expl = Explosion(hit.rect.center,"lg")
        #all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        r = Rock()    #撞擊石頭後增加石頭
        all_sprites.add(r)
        rocks.add(r)
    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
        player.health -= 20
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            player.hide()
    hits = pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 50
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            player.gunup()



    if player.lives == 0:
        show_init = True
    #顯示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,16)
    draw_lives(screen,player.lives,player_mini_img,WIDTH -100,15)
    pygame.display.update()

pygame.quit()





