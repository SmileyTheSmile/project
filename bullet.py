import pygame,os
from math import atan2,pi,sin,cos

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message) 

class Bullet(pygame.sprite.Sprite):
    def __init__(self,default_pos):
        super().__init__()
        self.image = load_image('bullet1.png')
        self.rect = self.image.get_rect() 
        self.rect.x,self.rect.y = default_pos[0],default_pos[1]
        self.angle = 0
        self.speed = 10
        self.shot = False
        
    def change_default_pos(self,player):
        self.rect.x,self.rect.y = player.rect.center[0]-2,player.rect.center[1]-2
    def shoot(self,pos):
        self.shot = True
        self.angle = self.get_angle(pos)
    
    def get_angle(self, destination):
        x_dist = destination[0] - self.rect.center[0]
        y_dist = destination[1] - self.rect.center[1]
        return atan2(-y_dist, x_dist) % (2 * pi)    

    def move(self):
        self.rect.center = (self.rect.center[0] + (cos(self.angle) * self.speed),
                self.rect.center[1] - (sin(self.angle) * self.speed))
    
#
class Bullet_group(pygame.sprite.Group):
    def __init__(self, bullets_number):
        super().__init__() 
        for i in range(bullets_number):
            self.add(Bullet((260,260)))

    def update(self,player,level,pos):
        for i in self.sprites():
            if i.shot:
                n1, n2 = i.rect.x, i.rect.y         
                if 0 < n1-1 and n1+1 < 512 and 0 < n2-1 and n2+1 < 512:
                    if not pygame.sprite.spritecollideany(i,level):
                        i.move()
                    else: 
                        i.shot = False
                        i.change_default_pos(player)                    
                else: 
                    i.shot = False
                    i.change_default_pos(player)
            else: i.change_default_pos(player)