import pygame as pg
from pygame.locals import *
import random
# from PIL import Image

# from pygame import Group

screen_width=600
screen_height=700
enemy_cooldown=1000
last_bullet=pg.time.get_ticks() 

screen=pg.display.set_mode((screen_width,screen_height))
pg.display.set_caption('Space Invadors')

clock=pg.time.Clock()

class SpaceInvadors(pg.sprite.Sprite):

    def __init__(self,x_pos,y_pos,total_lives):

        pg.sprite.Sprite.__init__(self)
        self.image= pg.image.load("Space Invaders 1.png")
        self.rect= self.image.get_rect()
        self.rect.topright=[x_pos,y_pos]
        # self.lives=total_lives
        # self.lives_remaining=total_lives
        # self.score=0

        # to get time in milliseconds 
        self.last_shot=pg.time.get_ticks()
    
    def move_spaceship(self):
        get_key=pg.key.get_pressed()

        if get_key[pg.K_LEFT] and self.rect.left>0:
            self.rect.x -=8
        if get_key[pg.K_RIGHT] and self.rect.right<screen_width:
            self.rect.x +=8

        long_shot=100
        

        # bullet=Bullets(self.rect.centerx,self.rect.top)
        # bullet_group.add(bullet)
        # bullet.move_bullet()

        current_time=pg.time.get_ticks()

        if get_key[pg.K_SPACE] and current_time-self.last_shot > long_shot:
            
            bullet=Bullets(self.rect.centerx,self.rect.top)
            bullet_group.add(bullet)
            bullet.update()
            self.last_shot=current_time

        self.mask=pg.mask.from_surface(self.image)

        pg.draw.rect(screen,(115,0,0),(self.rect.x,(self.rect.bottom+10),self.rect.width,15))

class Bullets(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("bullet_4.png")
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        # score_1=0


    def update(self):
        # print(self.rect.y)
        self.rect.y-=5

        if self.rect.bottom<150:
            self.kill()

        if pg.sprite.spritecollide(self,enemies_group,True):
            self.kill()
            global score_1
            score_1=score_1+10


class Enemies(pg.sprite.Sprite):

    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("enemies.png")
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.move_counter=0
        self.move_direction=1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter+=1

        if abs(self.move_counter)>50:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class EnemiesBullets(pg.sprite.Sprite):

    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("enemy_bullet.png")
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]

    def update(self):
        self.rect.y += 1
        if self.rect.top>screen_height:
           self.kill()

        if pg.sprite.spritecollide(self,spaceship_group,False,pg.sprite.collide_mask):
            self.kill()
            global total_lives
            total_lives-=1
            # spaceship.lives_remaining-=1


pg.init()

spaceship_group=pg.sprite.Group()
bullet_group=pg.sprite.Group()
enemies_group=pg.sprite.Group()
enemies_bullets=pg.sprite.Group()

def draw_enemies():
    # print("jhfkj")
    for i in range(5):
        for j in range(5):
            enemy=Enemies(100+j*100,100+i*70)
            enemies_group.add(enemy)

draw_enemies()


global level_no,score_1,total_lives
level_no=1
score_display=0
score_1=0
total_lives=3
font = pg.font.Font('freesansbold.ttf', 32)

spaceship=SpaceInvadors(int(screen_width/2),screen_height - 100,2)
# bullets=Bullets(2,4)
spaceship_group.add(spaceship)

game=True
while game:

    clock.tick(60)
    screen.fill("black")
    level = font.render('Level '+str(level_no), True,(255, 102, 51))
    
    score = font.render('Score '+str(score_1), True,(255, 102, 51))
    # score = font.render('Score '+str(score_display), True,(255, 102, 51))
    score_center=score.get_rect()
    score_center.left=250

    lives=font.render('Lives '+str(total_lives), True,(255, 102, 51))
    lives_center=lives.get_rect()
    lives_center.left=450
    
    screen.blit(score,score_center)
    screen.blit(level,level.get_rect())
    screen.blit(lives,lives_center)



    current_time=pg.time.get_ticks()

    if len(enemies_group)>0 and len(enemies_bullets) <4 and current_time-last_bullet>enemy_cooldown :
        shot_enemy=random.choice(enemies_group.sprites())
        enemies_bullet=EnemiesBullets(shot_enemy.rect.centerx,shot_enemy.rect.bottom)
        enemies_bullets.add(enemies_bullet)
        last_bullet=current_time
        count_level=0

    if(len(enemies_group)==0 and count_level==0):
        level_no+=1
        text = font.render('Level '+str(level_no), True,(255, 102, 51))
        count_level=1

    for event in pg.event.get():
        if event.type==pg.QUIT:
                game=False

    spaceship.move_spaceship()
    bullet_group.update()
    enemies_group.update()
    enemies_bullets.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemies_group.draw(screen)
    enemies_bullets.draw(screen)

    pg.display.update()

pg.quit()


# image = Image.open('bullet_4.png')
# new_image = image.resize((10, 10))
# new_image.save('enemy_bullet.png')
