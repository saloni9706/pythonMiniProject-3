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
    
    # def draw_rect(self):
    #     pg.draw.rect(screen,(0, 0, 255), (50,450, 50, 50))
    #     pg.draw.rect(screen,(0, 0, 255), (350,450, 50, 50))

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
        if pg.sprite.spritecollide(self,obs_grp,True):
            self.kill()
                # global score_1
                # score_1=score_1+10


class Enemies(pg.sprite.Sprite):

    def __init__(self,x,y,i):
        pg.sprite.Sprite.__init__(self)
       
        self.image=pg.image.load("enemy_"+i+".png")
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
        # if pg.sprite.spritecollide(self,spaceship_group,True):
        #     pass
class obstacles(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
       
        self.image=pg.image.load("enemy_1.png")
        self.rect=self.image.get_rect()
    def draw_rect(self):
        
        pg.draw.rect(screen,(0, 0, 255), (50,450, 50, 50))
        pg.draw.rect(screen,(0, 0, 255), (350,450, 50, 50))
    
    def update(self):
        # if pg.sprite.spritecollide(self,bullet_group,True):
        #     self.kill()
        if pg.sprite.spritecollide(self,enemies_bullets,True):
            self.kill()
        if pg.sprite.spritecollide(self,bullet_group,True,pg.sprite.collide_mask):
            self.kill()


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
        if pg.sprite.spritecollide(self,obs_grp,False,pg.sprite.collide_mask):
            self.kill()
        #  if pg.sprite.spritecollide(self,obs_grp,True):
        #     self.kill()
            


pg.init()

spaceship_group=pg.sprite.Group()
bullet_group=pg.sprite.Group()
enemies_group=pg.sprite.Group()
enemies_bullets=pg.sprite.Group()
obs_grp=pg.sprite.Group()

def draw_enemies(level_no):
    # print("jhfkj")
    if(level_no==1):
        for i in range(3):
            for j in range(3):
                enemy=Enemies(100+j*100,100+i*70,str(i+1))
                enemies_group.add(enemy)

    if(level_no==2):
        for i in range(4):
            for j in range(4):
                enemy=Enemies(100+j*100,100+i*70,str(i+1))
                enemies_group.add(enemy)

    if(level_no==3):
        for i in range(5):
            for j in range(5):
                enemy=Enemies(100+j*100,100+i*70,str(i+1))
                enemies_group.add(enemy)

# draw_enemies()


global level_no,score_1,total_lives
level_no=1
score_display=0
score_1=0
total_lives=3
font = pg.font.Font('freesansbold.ttf', 32)

spaceship=SpaceInvadors(int(screen_width/2),screen_height - 100,2)
# bullets=Bullets(2,4)
spaceship_group.add(spaceship)
obs=obstacles()
obs_grp.add(obs)
call_function=1
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
    
    if total_lives==0 :
            game_over=font.render("Game Over !!",True,(236,228,228))
            screen.blit(game_over,(200,400))
            pg.time.wait(2000)
            # game=False

    screen.blit(score,score_center)
    screen.blit(level,level.get_rect())
    screen.blit(lives,lives_center)

    if level_no==1 and call_function==1:
        pg.time.wait(1000)
        draw_enemies(level_no)
        call_function=0 
    if level_no==2 and call_function==1:
        pg.time.wait(1000)
        draw_enemies(level_no)
        call_function=0

    if level_no==3 and call_function==1:
        pg.time.wait(1000)
        draw_enemies(level_no)
        call_function=0    

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
        call_function=1

    

    for event in pg.event.get():
        if event.type==pg.QUIT:
                game=False
        


    spaceship.move_spaceship()
    obs.draw_rect()
    obs_grp.update()
    bullet_group.update()
    enemies_group.update()
    enemies_bullets.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    enemies_group.draw(screen)
    enemies_bullets.draw(screen)

    pg.display.update()

pg.quit()


# image = Image.open('enemy.png')
# new_image = image.resize((50, 50))
# new_image.save('enemy_2.png')
