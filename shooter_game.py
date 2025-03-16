# tODO Создай собственный Шутер!

from pygame import *
from random import randint



class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__()
        self.image  = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.speed=speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y)) 
    def collidepoint (self,x,y):
        return self.rect.collidepoint(x,y)    


class Player(GameSprite):
    def update(self):
        keys= key.get_pressed()
        if keys[K_LEFT]and self .rect.x >10:
            self.rect.x -=self.speed
        if keys[K_RIGHT]and self .rect.x <700-10-self.rect.width:
            self.rect.x +=self.speed    
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.y,15,30,5)
        bullets.add(bullet)
        


class Enamy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x=randint(10,700-10-self.rect.height)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)
            lost += 1

class Bullet (GameSprite):
    def update(self):    
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
                 
bullets = sprite.Group()        

player = Player('rocket.png',316,400,68,100,5)
e_count = 6
enemyes = sprite.Group()
for i in range(e_count):
    enamy = Enamy('ufo.png',randint(10,700-10-70),-40,70,40,randint(2,5))
    enemyes.add(enamy)

button  =GameSprite('btn.png',300,200,100,50,0)


window = display.set_mode((700,500))
display.set_caption('Шутер')




#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'),(700,500))



# под музыке
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()



font.init()
#font1 = font.Font(None,36)
font1 = font.SysFont('Arial',36)




game = True
finih = True
menu = True
lost = 0
skor = 0
clock = time.Clock()
FPS = 60

while game:
  

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE :     
                player.fire()
    if menu:
        window.blit(background,(0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0],pos[1]):
                menu = False
                finih= False

    if not finih:    


        window.blit(background,(0,0))
        player.update()
        player.reset()
        enemyes.update()
        enemyes.draw(window)
        bullets.update()
        bullets.draw(window)
        lost_enemy = font1.render('Пpопущенно '+ str(lost),1,(255,255,255))
        window.blit(lost_enemy ,(10,10))
        skor_enemy = font1.render('убито '+ str(skor),1,(255,255,255))
        window.blit(skor_enemy ,(10,40))
        

        sprite_list = sprite.groupcollide(enemyes,bullets,True,True)
        for i in range(len(sprite_list)):
            skor +=1
            enamy = Enamy('ufo.png',randint(10,700-10-70),-40,70,40,randint(2,5))
            enemyes.add(enamy)
            if skor >= 10:
                finih = True
                text_win = font1.render("wesyr",1,(255,255,255))
                window.blit(text_win,(350,250))
                sprite_list = sprite.spritecollide(player, enemyes, True)
            if lost>=10 or len(sprite_list)>0:
                finish=True
                text_lose = font1.render('ПРОИГРЫШ!', 1, (255,255,255))
                window.blit(text_lose, (350,250))
    display.update()  
    clock.tick(FPS)          

