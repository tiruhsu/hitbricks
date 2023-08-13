import pygame
import random
import time
import os
#遊戲初始化和創建視窗
FPS=60
WHITE = (255,255,255)
GREEN = (0,255,0)
Red=(255,0,0)
YELLOW = (255,255,0)
BLACK=(0,0,0)
WIDTH = 640
HEIGHT = 480
BLUE=(50, 50, 250)
Purple = (148, 0, 211)
Cyan = (0,255,255)
Pink = (255, 192, 203)
LightGray =(211,211,211)
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_COLOR = (200, 100, 0)
need_new_bricks = False
twobrickhitlevel = 2 
pygame.init()
hitkit = 0
screen =  pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("打磚塊")
clock = pygame.time.Clock()
show_init = True
running = True
ballspeedx = 4
ballspeedy = 4
#載入圖片
font_name = os.path.join("font.ttf")
def draw_text(surf, point, text , size,x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text,True, WHITE)
    point_surface = font.render(point,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface , text_rect)
    surf.blit(point_surface,(x-90,y))
def normal_text(surf, text ,size,x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text,True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface , text_rect)
def draw_init():
    hitkit=0
    screen.fill(BLACK)
    normal_text(screen,'打磚塊',50,WIDTH/2,HEIGHT/4)
    normal_text(screen,'← → 移動玩家磚塊',22,WIDTH/2,HEIGHT/6)
    normal_text(screen,'案任意建開始',18,WIDTH/2,HEIGHT*3/4)
    normal_text(screen,'黃色，球變大，紫色，球變小，青色，玩家變大',20,WIDTH/2,HEIGHT-200)
    normal_text(screen,'灰色，球減慢，粉色，玩家變小',20,WIDTH/2,HEIGHT-170)
    pygame.display.update()
    waiting = True
    while waiting :
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                quit()                
            elif event.type == pygame.KEYUP:
                hitkit+=1
                if hitkit==2:
                    waiting = False
                    
#sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT / 2)
        self.speedx = ballspeedx
        self.speedy = ballspeedy
        self.ballsped = 1
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx *= -1
        if self.rect.left<0:
            self.rect.left = 0
        if self.rect.right> WIDTH:
            self.rect.right = WIDTH    
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speedy *= -1
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom>HEIGHT:
            self.rect.bottom = HEIGHT     
    def ballspeed(self,time):   
        if time >3600*self.ballsped:
            if self.speedy >0:
                self.speedy+=1
            elif self.speedy <0:
                self.speedy-=1
            if self.speedx >0:
                self.speedx+=1
            elif self.speedx <0:
                self.speedx-=1      
            self.ballsped+=1
    def big(self,x,y): 
        self.image = pygame.Surface((40, 40))  # 修改大小为 40x40
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
    def small(self,x,y):
        self.image = pygame.Surface((10, 10))  # 修改大小为 10x10
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
    def smallspeedy(self):
        if abs(self.speedx) <4  or abs(self.speedy) < 4:
            if self.speedy >0:
                self.speedy=4
            elif self.speedy <0:
                self.speedy=-4
            if self.speedx >0:
                self.speedx=4
            elif self.speedx <0:
                self.speedx=-4 
        if self.speedy >0:
            self.speedy-=1
        elif self.speedy <0:
            self.speedy+=1
        if self.speedx >0:
            self.speedx-=1
        elif self.speedx <0:
            self.speedx+=1               
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(BRICK_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = 1
    def shoot(self):
        persent = random.randint(1,100)
        prop=Prop(self.rect.centerx,self.rect.top)
        if persent <=20 :
            prop.image.fill(YELLOW)
            prop.prop = 1
        if 20 < persent <= 40 :
            prop.image.fill(Purple)
            prop.prop = 2
        if 40 < persent <= 60 :
            prop.image.fill(Cyan)
            prop.prop = 3
        if 60 < persent <= 80 :
            prop.image.fill(Pink)
            prop.prop = 4     
        if 80 < persent <= 100 :
            prop.image.fill(LightGray)
            prop.prop = 5
        all_sprites.add(prop)
        props.add(prop)               
    
class TwoBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = 1
        self.hits = 0 
    def hit(self):
        self.hits += 1
        if self.hits >= twobrickhitlevel:
            self.kill()
            return True   
        return False
    def shoot(self):
        persent = random.randint(1,100)
        prop=Prop(self.rect.centerx,self.rect.top)
        if persent <=20 :
            prop.image.fill(YELLOW)
            prop.prop = 1
        if 20 < persent <= 40 :
            prop.image.fill(Purple)
            prop.prop = 2
        if 40 < persent <= 60 :
            prop.image.fill(Cyan)
            prop.prop = 3
        if 60 < persent <= 80 :
            prop.image.fill(Pink)
            prop.prop = 4     
        if 80 < persent <= 100 :
            prop.image.fill(LightGray)
            prop.prop = 5
        all_sprites.add(prop)
        props.add(prop)
          
           
class Die(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((640,1))
        self.image.fill(Red)
        self.rect=self.image.get_rect()
        self.rect.centerx= WIDTH/2
        self.rect.bottom = HEIGHT               
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.long = 100
        self.image = pygame.Surface((self.long,30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH-80
        self.rect.bottom = HEIGHT-10
        self.speedx = 12
        self.bigtime = 3600
        self.time =0
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx      
        if self.rect.left < 0 :
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def big(self):
        self.image = pygame.Surface((self.long*2,30))  
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=self.rect.center) 
    def small(self):
        self.image = pygame.Surface((self.long/2,30))  # 修改大小为 40x40
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=self.rect.center) 
class Prop(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 4
        self.prop = 1
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT: 
            self.kill()
    def Yellow (self):
            ball.big(ball.rect.x, ball.rect.y)
    def Purple (self):            
            ball.small(ball.rect.x, ball.rect.y)
    def Cyan (self):              
            player.big()
    def LightGray (self):         
            player.small()
    def Pink (self):                 
            ball.smallspeedy()                                                         
#磚塊生成  
def Bricksgenerate() :
    for row in range(4):
        for col in range(9):
            brickpersent  = random.randint(1,100)
            if brickpersent>30:
                brick = Brick(col * (BRICK_WIDTH + 5) + 30, row * (BRICK_HEIGHT + 5) + 50)
                bricks.add(brick)
                all_sprites.add(brick)
            if brickpersent<=30:
                twobrick = TwoBrick(col * (BRICK_WIDTH + 5) + 30, row * (BRICK_HEIGHT + 5) + 50)
                twobricks.add(twobrick)
                all_sprites.add(twobrick)
def custom_collide_rect(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)                            
#spirtgroup初始化    
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
twobricks= pygame.sprite.Group()
props = pygame.sprite.Group()
die=Die()
player = Player()
ball = Ball()
all_sprites.add(player, ball,die)
score = 0
scoretext = 'score: '
Bricksgenerate()
time = 0
need_new_bricks = False                 
#遊戲迴圈
while running:
    #等待畫面   
    if show_init:
            draw_init()
            show_init = False
            #小心  
            all_sprites = pygame.sprite.Group()
            bricks = pygame.sprite.Group()
            twobricks= pygame.sprite.Group()
            props = pygame.sprite.Group()
            die=Die()
            player = Player()
            ball = Ball()
            all_sprites.add(player, ball,die)
            score = 0
            scoretext = 'score: '
            Bricksgenerate()
            time = 0
            need_new_bricks = False
                  
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False            
    #更新遊戲
    all_sprites.update()
    #ballspeedtime
    time+=1
    ball.ballspeed(time)
    #player and ball
    if pygame.sprite.collide_rect(player, ball):
        if ball.speedy > 0:
            ball.rect.bottom = player.rect.top
        else:
            ball.rect.top = player.rect.bottom
        ball.speedy *= -1    
    #player and  prop
    hit_prop = pygame.sprite.spritecollide(player, props, False, collided=custom_collide_rect)
    if  hit_prop :
        for prop in props:
            if prop.prop==1:
                prop.Yellow()
            if prop.prop==2:
                prop.Purple()
            if prop.prop==3:
                prop.Cyan()
            if prop.prop==4:
                prop.LightGray()
            if prop.prop==4:
                prop.Pink()            
            prop.kill()
    #twobrick and ball 
    hit_bricks = pygame.sprite.spritecollide(ball, bricks,True)
    hit_twobricks = pygame.sprite.spritecollide(ball,twobricks,False)
    if hit_twobricks:
        ball.speedy *= -1
        for twobrick in hit_twobricks:
            scorebool = twobrick.hit()
            if scorebool:
                score+=twobrick.score
                whethershoot = random.randint(1,100) 
                if whethershoot <= 70:
                    twobrick.shoot()
                    

    #brick and ball                  
    if hit_bricks:
        whethershoot = random.randint(1,100) 
        for brick in hit_bricks:
            score+=brick.score
            if whethershoot <= 30:
                brick.shoot()
        ball.speedy *= -1
    #need new brick    
    if len(bricks)==0 and len(twobricks) ==0:
        need_new_bricks = True
    hit_die = ball.rect.colliderect(die.rect)
    if need_new_bricks and ball.rect.y>240:
        Bricksgenerate()
        need_new_bricks = False        

    if hit_die:
       show_init = True     
    #畫面顯示
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen,str(scoretext),str(score),25, 100 , 10)
    pygame.display.update()
pygame.quit()    

