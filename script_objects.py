from script_variables import *
import math
import random

pygame.display.init()
pygame.display.set_mode((screenWidth, screenHeight))

game_folder = os.path.dirname(__file__)  
img_folder = os.path.join(game_folder, 'img')

circle_large = pygame.image.load(os.path.join(img_folder, "circle.png")).convert_alpha()

bg_cave = pygame.image.load(os.path.join(img_folder, "background.png")).convert()
apple = pygame.image.load(os.path.join(img_folder, "apple.png")).convert_alpha()
potion = pygame.image.load(os.path.join(img_folder, "potion.png")).convert_alpha()

game_over_screen = pygame.image.load(os.path.join(img_folder, "game over transparent.png")).convert_alpha()

play_white = pygame.image.load(os.path.join(img_folder, "play_white.png")).convert()
play_black = pygame.image.load(os.path.join(img_folder, "play_black.png")).convert()

heart = pygame.image.load(os.path.join(img_folder, "heart_1.png")).convert_alpha()

player_anim = {'walk_up': [] , 'walk_down': [] , 'walk_left': [] , 'walk_right': []}
        
img2 = pygame.image.load(os.path.join(img_folder, "player.png")).convert_alpha()
#img2.set_colorkey((255,255,255,255))

for frame in range(8):
    img_cut = img2.subsurface(pygame.Rect((320+40*frame,0),(40,40)))
    player_anim['walk_down'].append(img_cut)    

for frame in range(8):
    img_cut = img2.subsurface(pygame.Rect((960+40*frame,0),(40,40)))
    player_anim['walk_up'].append(img_cut)

for frame in range(8):
    img_cut = img2.subsurface(pygame.Rect((640+40*frame,0),(40,40)))
    player_anim['walk_left'].append(img_cut)

for frame in range(8):
    img_cut = img2.subsurface(pygame.Rect((40*frame,0),(40,40)))
    player_anim['walk_right'].append(img_cut)


enemy_anim = {'idle': [] , 'run_right': [], 'run_left': []}
    
for key in enemy_anim:
    if key == 'run_left':
        for i in range(4):
            filename = "big_demon_run_anim_f{0}.png".format(i)
            img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
            img = pygame.transform.flip(img,True,False)
            #img.set_colorkey(black)
            enemy_anim[key].append(img)
    elif key == 'run_right':
        for i in range(4):
            filename = "big_demon_run_anim_f{0}.png".format(i)
            img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
            #img.set_colorkey(black)
            enemy_anim[key].append(img)
    elif key == 'idle':
        for i in range(4):
            filename = "big_demon_idle_anim_f{0}.png".format(i)
            img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
            #img.set_colorkey(black)
            enemy_anim[key].append(img)



class RectBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size):
        super().__init__()
        
        self.char = None
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        self.image.set_alpha(150)
        
        pygame.draw.rect(self.image, color, [0, 0, size[0], size[1]])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        #self.rect.x += 1
        pass

alpha_block = 220
class ImageBox(pygame.sprite.Sprite):
    def __init__(self, char, color, pos, size, width = 0, delay = 0, bg_color = black, static = False, flash = False):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        
        self.bgcolor = bg_color
        self.char = char
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        
        self.static = static
        
        self.flash = flash
        self.color_tense = 1
        
        self.cur_color = 0
        
        self.updating = True
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps
        
        self.delay = delay
        self.delay_lasttick = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    
    def update(self):
        if (pygame.time.get_ticks() < self.delay_lasttick + self.delay):
            pass
        elif self.static == False:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.blit(pygame.transform.scale(self.char, (self.size[0],self.size[1])),(0,0))
                if self.flash: pygame.draw.rect(self.image, [7*self.color_tense*self.anim_frame*(1 if self.cur_color == 0 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 1 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 2 else 0)], [0, 0, self.size[0], self.size[1]])  
                else: self.image.set_alpha((6-self.anim_frame)/6*alpha_block)
                
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                self.anim_frame -= 1
                
            if self.anim_frame == 0:
                self.static = True
                
        elif self.static:
            self.image = pygame.transform.scale(self.char, (int(self.size[0]),int(self.size[1])))
            self.updating = False


class ColorBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, width, color_tense = 1):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(black)
        self.image.set_alpha(128)
        
        self.color = color
        self.pos = pos
        self.size = size
        self.width = width
        self.color_tense = color_tense
        
        self.cur_color = 0
        
        self.anim_frame = 6
        self.anim_lasttick = pygame.time.get_ticks()
        self.anim_speed = fps*3
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = True
        
    def update(self):
        if self.anim_frame == 6:
            self.cur_color += 1
            self.cur_color %= 3
        
        if self.anim_frame != 0:
            if (self.anim_lasttick + self.anim_speed < pygame.time.get_ticks()):
                self.anim_lasttick = pygame.time.get_ticks()
                self.image.set_alpha(int(128*(self.anim_frame/6)))
                pygame.draw.rect(self.image, [7*self.color_tense*self.anim_frame*(1 if self.cur_color == 0 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 1 else 0) , 7*self.color_tense*self.anim_frame*(1 if self.cur_color == 2 else 0)], [0, 0, self.size[0], self.size[1]])  
                pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
                pygame.draw.rect(self.image, self.color, [0-3, 0-3, self.size[0]+3, self.size[1]+3], self.width+3)
                self.anim_frame -= 1
                
                
        elif self.anim_frame == 0:
            pygame.draw.rect(self.image, black, [0, 0, self.size[0], self.size[1]])  
            pygame.draw.rect(self.image, self.color, [0, 0, self.size[0], self.size[1]], self.width)
            self.updating = False

class PlayerBox(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        
        self.size = size
        self.image = pygame.transform.scale(player_anim['walk_down'][0], (self.size[0],self.size[1]))
        
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.frame = 0
        self.framerate = int(fps*1.5)
        self.lasttick = pygame.time.get_ticks()
        
        self.move_dir = idle
        self.last_dir = right
    
    def move_anim(self):
        
        if self.move_dir == down:
            self.rect.y += 3
            self.last_dir = down
            
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(player_anim['walk_down'])
                
                pos2 = self.rect.topleft
                size = self.rect
                self.image = pygame.transform.scale(player_anim['walk_down'][self.frame], (self.size[0],self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
        
        elif self.move_dir == up:
            self.rect.y -= 3
            self.last_dir = up
            
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(player_anim['walk_up'])
                
                pos2 = self.rect.topleft
                size = self.rect
                self.image = pygame.transform.scale(player_anim['walk_up'][self.frame], (self.size[0],self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
                
        elif self.move_dir == left:
            self.rect.x -= 3
            self.last_dir = left
            
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(player_anim['walk_left'])
                
                pos2 = self.rect.topleft
                size = self.rect
                self.image = pygame.transform.scale(player_anim['walk_left'][self.frame], (self.size[0],self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
                
        elif self.move_dir == right:
            self.rect.x += 3
            self.last_dir = right
            
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(player_anim['walk_right'])
                
                pos2 = self.rect.topleft
                size = self.rect
                self.image = pygame.transform.scale(player_anim['walk_right'][self.frame], (self.size[0],self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
                
        else:
            self.frame = 0
            
            pos2 = self.rect.topleft
            size = self.size
            if self.last_dir == down:
                self.image = pygame.transform.scale(player_anim['walk_down'][self.frame], (size[0],size[1]))
            if self.last_dir == up:
                self.image = pygame.transform.scale(player_anim['walk_up'][self.frame], (size[0],size[1]))
            if self.last_dir == left:
                self.image = pygame.transform.scale(player_anim['walk_left'][self.frame], (size[0],size[1]))
            if self.last_dir == right:
                self.image = pygame.transform.scale(player_anim['walk_right'][self.frame], (size[0],size[1]))
            self.rect = self.image.get_rect()
            self.rect.topleft = pos2
              
    def update(self):
        
        self.move_anim()


class EnemyBox(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        
        self.speed = random.randint(1500,2500)/1000
        self.size = size
        self.image = pygame.transform.scale(enemy_anim['idle'][0], (self.size[0],self.size[1]))
        
        self.target = None
        self.angle = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.frame = 0
        self.framerate = int(fps*1.5)
        self.lasttick = pygame.time.get_ticks()
        
        self.move_dir = idle
        self.last_dir = right
    
    def compute_move(self):
        if self.target != None:
            x = self.target[0] - self.rect.center[0]
            y = self.target[1] - self.rect.center[1]
            self.angle = math.atan2(y, x)
            
    def collision(self):
        if self.target != None:
            self.image.set_alpha(0)
            self.rect.y -= int(50 * math.sin(self.angle))
            self.rect.x -= int(50 * math.cos(self.angle))
        
        if pygame.time.get_ticks() > (self.lasttick + self.framerate):
            self.lasttick = pygame.time.get_ticks()
            
            self.frame += 1
            self.frame %= len(enemy_anim['run_right'])
            
            pos2 = self.rect.topleft
            size = self.rect
            self.image = pygame.transform.scale(enemy_anim['run_right'][self.frame], (self.size[0],self.size[1]))
            self.rect = self.image.get_rect()
            self.rect.topleft = pos2
            
            #print (self.rect.center,self.target)
            if self.rect.center == self.target:
                self.target = None
    
    def move_anim(self):    
        
        if self.target != None:
            self.rect.y += int(self.speed * math.sin(self.angle))
            self.rect.x += int(self.speed * math.cos(self.angle))
            
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(enemy_anim['run_right'])
                
                pos2 = self.rect.topleft
                size = self.rect
                
                if (math.pi/2) > abs(self.angle):
                    self.image = pygame.transform.scale(enemy_anim['run_right'][self.frame], (self.size[0],self.size[1]))
                else:
                    self.image = pygame.transform.scale(enemy_anim['run_left'][self.frame], (self.size[0],self.size[1]))   
                    
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
            
            #print (self.rect.center,self.target)
            if self.rect.center == self.target:
                self.target = None
                
        
        else:         
            if pygame.time.get_ticks() > (self.lasttick + self.framerate):
                self.lasttick = pygame.time.get_ticks()
                
                self.frame += 1
                self.frame %= len(enemy_anim['idle'])
                
                pos2 = self.rect.topleft
                size = self.rect
                self.image = pygame.transform.scale(enemy_anim['idle'][self.frame], (self.size[0],self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = pos2
                
                
              
    def update(self):
        
        self.compute_move()
        self.move_anim()