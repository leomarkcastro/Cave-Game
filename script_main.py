import pygame
from script_objects import *
import random

#Scene A = Title
#Scene B = Main Game
#Scene C = Game Over

sw = screenWidth
sh = screenHeight

print (sw,sh)

def dt(x):
    x = list(x)
    x[0] = int(x[0] / 800 * sw)
    x[1] = int(x[1] / 600 * sh)
    
    return (x[0],x[1])

def dt2(x,y):
    x = list(x)
    x[0] = int(x[0] / 800 * sw)
    x[1] = int(x[1] / 600 * sh)
    
    y = list(y)
    y[0] = int(y[0] / 800 * sw)
    y[1] = int(y[1] / 600 * sh)
    
    return (x[0],x[1]),(y[0],y[1])

class CaveGame:
    def __init__(self):
        self.gameDisplay = pygame.display.set_mode((screenWidth, screenHeight), display_flags)
        pygame.display.set_caption(screenCaption)
        
        self.clock = pygame.time.Clock()
        self.running = 'A'
        
        self.game_load()
        self.SceneLooper()
    
    def game_load(self):
        self.save_dict = json_load()
            
        self.settings_dict = json_load('settings.json')
    
    def SceneLooper(self):
        while len(self.running) != 0:
            if self.running == 'A':
                self.SceneA()
            elif self.running == 'B':
                self.SceneB()
            elif self.running == 'C':
                self.running = 'B'
    
    def SceneA(self):
        def game_start():
            
            playmusic(music_array['main_menu'],start_at = 3) if self.settings_dict["music"] else None
            self.all_sprite = pygame.sprite.Group()
            
            self.all_sprite.add(ImageBox(play_black,black,*dt2([0,0],[800,600]),static=True))
        
        def game_control():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = 'B'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(*dt((296,263)),*dt((502-296,349-263))).collidepoint(pygame.mouse.get_pos()):
                        self.running = 'B'
        
        def game_system():
            
            if pygame.Rect(*dt((296,263)),*dt((502-296,349-263))).collidepoint(pygame.mouse.get_pos()):
                self.all_sprite.empty()
                self.all_sprite.add(ImageBox(play_white,black,*dt2([0,0],[800,600]),static=True))
            else:
                self.all_sprite.empty()
                self.all_sprite.add(ImageBox(play_black,black,*dt2([0,0],[800,600]),static=True))
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
            
        def game_display():
            self.gameDisplay.fill(white)
            
            self.all_sprite.draw(self.gameDisplay)
            
            if self.save_dict["highscore"] != None:
                text, textRect = textdisplay('HighScore : {0}'.format(self.save_dict["highscore"]), font_color[3], font_typo[3])
                textRect.center = pygame.Rect(0,0,screenWidth,screenHeight).center
                textRect.top = textRect.top + 75
                self.gameDisplay.blit(text, textRect)
            
            pygame.display.flip()
        
        def game_loop():
            game_start()
            
            while self.running == 'A':
                game_control()
                game_system()
                game_display()
                
                self.clock.tick(fps)
        
        game_loop()
 
    
    def SceneB(self):
        def game_start():
            playmusic(music_array['main_game'],repeat=-1) if self.settings_dict["music"] else None
            
            self.score = 0
            self.timer = 45
            self.life = 5
            self.timertick = pygame.time.get_ticks()
            
            self.all_sprite = pygame.sprite.Group()
            self.enemy_sprite = pygame.sprite.Group()
            self.apple_sprite = pygame.sprite.Group()
            self.potion_sprite = pygame.sprite.Group()
            self.shade_group = pygame.sprite.Group()
            
            self.all_sprite.add(ImageBox(bg_cave,black,dt([0,0]),dt([800,600]),static=True))
            
            self.box_effect  = ColorBox(black,*dt2([0,0],[800,600]),1,color_tense = 3)
            self.all_sprite.add(self.box_effect)
            
            self.player = PlayerBox(*dt2((100,100),(50,50)))
            self.all_sprite.add(self.player)
            
            for i in range(self.settings_dict['monster_start']):
                while True:
                        loc = dt([random.randint(150,650),random.randint(150,450)])
                        if self.player.rect.inflate(dt((-60,-60))).colliderect(pygame.Rect(*loc,120,120)):
                            continue
                        break
                enemy = EnemyBox(*dt2(loc,(120,120)))
                self.enemy_sprite.add(enemy)
                self.all_sprite.add(enemy)
            
            
            for i in range(self.settings_dict['apple_start']):
                while True:
                        loc = dt([random.randint(150,650),random.randint(150,450)])
                        if self.player.rect.inflate(dt((-60,-60))).colliderect(pygame.Rect(*loc,120,120)):
                            continue
                        break
                food = ImageBox(apple,black,*dt2(loc,(25,20)))
                self.apple_sprite.add(food)
                self.all_sprite.add(food)
            
            for i in range(self.settings_dict['potion_start']):
                while True:
                        loc = dt([random.randint(150,650),random.randint(150,450)])
                        if self.player.rect.inflate(dt((-60,-60))).colliderect(pygame.Rect(*loc,120,120)):
                            continue
                        break
                power = ImageBox(potion,black,*dt2(loc,(20,25)))
                self.potion_sprite.add(power)
                self.all_sprite.add(power)
            
            
            self.shade = ImageBox(circle_large,black,dt([0,0]),dt([1600*3,1200*3]),static=True)
            self.shade_group.add(self.shade)
            
            shade_heart = ImageBox(potion,black,dt([635,50]),dt([50,50]),static=True)
            self.shade_group.add(shade_heart)
            
            shade_apple = ImageBox(apple,black,dt([635,110]),dt([50,50]),static=True)
            self.shade_group.add(shade_apple)
            
            self.timer_rect = [0,0,0]
            
            for i in range(3):
                self.timer_rect[i] = RectBox(blue,*dt2((680+37*i,68),(35,25)))
                self.shade_group.add(self.timer_rect[i])
            
            for i in range(self.life):
                hearts = ImageBox(heart,black,dt([650+28*i,25]),dt([25,25]),delay = 250*i,static=True)
                self.shade_group.add(hearts)
        
        def game_control():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                if event.type == pygame.KEYDOWN:
                    if self.life >= 1:
                        if event.key == pygame.K_a:
                            self.player.move_dir = left
                        elif event.key == pygame.K_d:
                            self.player.move_dir = right
                        elif event.key == pygame.K_w:
                            self.player.move_dir = up
                        elif event.key == pygame.K_s:
                            self.player.move_dir = down
                        elif event.key == pygame.K_ESCAPE:
                            self.running = ''
                    else:
                        self.running = 'C'
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and self.player.move_dir == left:
                        self.player.move_dir = idle
                    elif event.key == pygame.K_d and self.player.move_dir == right:
                        self.player.move_dir = idle
                    elif event.key == pygame.K_w and self.player.move_dir == up:
                        self.player.move_dir = idle
                    elif event.key == pygame.K_s and self.player.move_dir == down:
                        self.player.move_dir = idle
        
        def game_system():

            if self.life >= 1:
            
                if (self.timertick + 1000 < pygame.time.get_ticks()) and (self.timer > 0):
                    self.timer -= 1
                    self.timertick = pygame.time.get_ticks()
    
                if self.timer > 30 and self.shade.size != dt((1600*3,1200*3)):
                    self.shade.size = dt((1600*3,1200*3))
                    self.shade.rect = pygame.Rect([0,0,self.shade.size[0],self.shade.size[1]])
                    self.shade.rect.center = self.player.rect.center
                    self.shade.updating = True
                elif 30 > self.timer > 15 and self.shade.size != dt((1600*2,1200*2)):
                    self.shade.size = dt((1600*2,1200*2))
                    self.shade.rect = pygame.Rect([0,0,self.shade.size[0],self.shade.size[1]])
                    self.shade.rect.center = self.player.rect.center
                    self.shade.updating = True
                elif 15 > self.timer and self.shade.size != dt((1600,1200)):
                    self.shade.size = dt((1600,1200))
                    self.shade.rect = pygame.Rect([0,0,self.shade.size[0],self.shade.size[1]])
                    self.shade.rect.center = self.player.rect.center
                    self.shade.updating = True
                
                if self.timer > 30:
                    self.timer_rect[0].image.set_alpha(150)
                    self.timer_rect[1].image.set_alpha(150)
                    self.timer_rect[2].image.set_alpha(int(25+125*((self.timer-30)/15)))
                elif 30 > self.timer > 15:
                    self.timer_rect[0].image.set_alpha(150)
                    self.timer_rect[1].image.set_alpha(int(25+125*((self.timer-15)/15)))
                elif 15 > self.timer:
                    self.timer_rect[0].image.set_alpha(int(25+125*((self.timer)/15)))
                
                if self.player.move_dir == left and self.player.rect.left < 0:
                    self.player.move_dir = idle
                if self.player.move_dir == right and self.player.rect.right > screenWidth:
                    self.player.move_dir = idle
                if self.player.move_dir == up and self.player.rect.top < 0:
                    self.player.move_dir = idle
                if self.player.move_dir == down and self.player.rect.bottom > screenHeight:
                    self.player.move_dir = idle
                
                self.shade.rect.center = self.player.rect.center
                
                if self.score // 3 > len(self.enemy_sprite)-1 and self.score != 0:
                    while True:
                        loc = dt([random.randint(150,650),random.randint(150,450)])
                        if self.player.rect.inflate(dt((-60,-60))).colliderect(pygame.Rect(*loc,120,120)):
                            continue
                        break
                    enemy = EnemyBox(*dt2(loc,(120,120)))
                    self.enemy_sprite.add(enemy)
                    self.all_sprite.add(enemy)
                    
                    power = ImageBox(potion,black,*dt2(loc,(20,25)))
                    self.potion_sprite.add(power)
                    self.all_sprite.add(power)
                
                for i in self.enemy_sprite:
                    if self.settings_dict['always_chase']:
                        i.target = self.player.rect.center 
                    else:
                        if i.rect.inflate(dt((200,200))).colliderect(self.player.rect):i.target = self.player.rect.center 
                        else: i.target = None
                    
                    if self.player.rect.inflate(dt((-60,-60))).colliderect(i.rect) and self.life >= 1:
                        self.box_effect.cur_color = 0
                        self.box_effect.anim_frame = 5
                        self.box_effect.updating = True
                        for j in self.shade_group:
                            if j.char == heart:
                                j.kill()
                                self.life -= 1
                                break
                            
                        beep_array['beep01'].play() if self.settings_dict['sound'] else None
                        i.collision()
                
                if self.life == 0:
                    self.player.kill()
                    if self.save_dict['highscore'] != None:
                        if self.score > self.save_dict['highscore']:
                            self.save_dict['highscore'] = self.score
                            json_save(self.save_dict)
                    else:
                        self.save_dict['highscore'] = self.score
                        json_save(self.save_dict) 
                        
                    for i in self.enemy_sprite:
                        i.target = (sw+200,sh+200)
                        
                    self.game_over = ImageBox(game_over_screen,black,*dt2([0,0],[500,275]),static=True)
                    self.game_over.rect.center = self.player.rect.center
                    self.game_over.rect.left -= dt((25,25))[0]
                    self.game_over.rect.top += dt((25,25))[1]
                    
                    self.all_sprite.add(self.game_over)
                    
                    playmusic(music_array['main_menu'],start_at = 3) if self.settings_dict["music"] else None
                    self.life = 0
                        
                
                for i in self.apple_sprite:
                    if self.player.rect.inflate(dt((-30,-30))).colliderect(i.rect):
                        i.kill()
                        beep_array['beep03'].play() if self.settings_dict['sound'] else None
                        self.box_effect.cur_color = 1
                        self.box_effect.anim_frame = 5
                        self.box_effect.updating = True
                        self.score += 1
                        food = ImageBox(apple,black,dt([random.randint(150,650),random.randint(150,450)]),dt([25,20]))
                        self.apple_sprite.add(food)
                        self.all_sprite.add(food)
                
                for i in self.potion_sprite:
                    if self.player.rect.inflate(dt((-30,-30))).colliderect(i.rect):
                        i.kill()
                        beep_array['beep02'].play() if self.settings_dict['sound'] else None
                        self.box_effect.cur_color = 2
                        self.box_effect.anim_frame = 5
                        self.box_effect.updating = True
                        self.timer += 15
                        
            for item in self.shade_group:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
                
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
           
        def game_display():
            self.gameDisplay.fill(white)
            
            self.all_sprite.draw(self.gameDisplay)
            self.shade_group.draw(self.gameDisplay)
            
            text, textRect = textdisplay('{0}'.format(self.score), font_color[1], font_typo[2])
            textRect.topleft = dt((688,81))
            self.gameDisplay.blit(text, textRect)
            
            if self.save_dict["highscore"] != None:
                text, textRect = textdisplay('HighScore : {0}'.format(self.save_dict["highscore"]), font_color[6], font_typo[3])
                textRect.topleft = dt((648,160))
                self.gameDisplay.blit(text, textRect)
            
            pygame.display.flip()
        
        def game_loop():
            game_start()
            
            while self.running == 'B':
                game_control()
                game_system()
                game_display()
                
                self.clock.tick(fps)
        
        game_loop()
    
    
    
    def SceneC(self):
        def game_start():
            
            playmusic(music_array['main_menu'],start_at = 3) if self.settings_dict["music"] else None
            self.all_sprite = pygame.sprite.Group()
            
            self.game_over = ImageBox(game_over_screen,black,*dt2([0,0],[600,400]),static=True)
            self.game_over.rect.center = self.player.rect.center
            
            self.all_sprite.add(self.game_over)
        
        def game_control():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = ''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = 'B'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(*dt((296,263)),*dt((502-296,349-263))).collidepoint(pygame.mouse.get_pos()):
                        self.running = 'B'
        
        def game_system():
            
            for item in self.all_sprite:
                if callable(getattr(item, 'update', None)):
                    if hasattr(item, 'updating'):
                        if item.updating == False:
                            continue
                    item.update()
            
        def game_display():

            self.all_sprite.draw(self.gameDisplay)
            
            if self.save_dict["highscore"] != None:
                text, textRect = textdisplay('HighScore : {0}'.format(self.save_dict["highscore"]), font_color[3], font_typo[3])
                textRect.center = pygame.Rect(0,0,screenWidth,screenHeight).center
                textRect.top = textRect.top + 75
                self.gameDisplay.blit(text, textRect)
            
            pygame.display.flip()
        
        def game_loop():
            game_start()
            
            while self.running == 'C':
                game_control()
                game_system()
                game_display()
                
                self.clock.tick(fps)
        
        game_loop()
        
CaveGame()  
pygame.quit()   