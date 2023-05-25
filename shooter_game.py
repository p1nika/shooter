#Создай собственный Шутер!

from pygame import *
from random import *

win = display.set_mode((700,500))
display.set_caption('Шутер')
biha = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 30)
lost = 0 
score = 0
goal = 10
piu = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
ship = Player('rocket.png', 200, 500-80, 65, 80, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

game = True
finish = False

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                piu.play()
                ship.fire()
                
    if not finish:
        win.blit(biha, (0,0))
        ship.reset()
        ship.update()
        monsters.draw(win)
        monsters.update()
        bullets.draw(win)
        bullets.update()
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_win = font2.render('Счeт:' + str(score), 1, (255,255,255))
        win.blit(text_win, (10, 40))
        win.blit(text_lose, (10, 10))
        display.update()

    time.delay(50)
    