import pygame
import os
import json

pygame.init()

game_folder = os.path.dirname(__file__)   

white = (255,255,255)
gray = (128,128,128)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
violet = (255,0,255)

up = 1
right = 2
down = 3
left = 4
idle = 0

def json_load(file = 'cave.json'):
    try:
        with open(file, "r") as read_file:
            savedict = json.load(read_file)
        return savedict
    
    except:
        if file == 'cave.json':
            savedict = {
                'highscore': None,
                }
            
            with open(file, "w+") as write_file:
                json.dump(savedict, write_file)
                
            return savedict
        
        elif file == 'settings.json':
            savedict = {
                'screen_w': 800,
                'screen_h': 600,
                'fullscreen': False,
                'gameTitle': "Cave Game",
                'always_chase':True,
                'moster_start':2,
                'apple_start':5,
                'potion_start':2,
                'music': True,
                'sound': True,
                
                }
            
            with open(file, "w+") as write_file:
                json.dump(savedict, write_file)
                
            return savedict

def json_save(savedict, file = os.path.join(game_folder, 'cave.json')):      
    with open(file, "w+") as write_file:
            json.dump(savedict, write_file)

settings = json_load('settings.json')
sdIxy = pygame.display.Info()

screenWidth = settings['screen_w']
screenHeight = settings['screen_h']
display_flags = (pygame.FULLSCREEN|pygame.HWACCEL) if settings['fullscreen'] else 0 #(pygame.FULLSCREEN|pygame.HWACCEL) if sdFull else 0
#print (sdIxy.current_w, sdIxy.current_h)
screenCaption = settings['gameTitle']
fps = 60

font_folder = os.path.join(game_folder, 'font')

font_array = {
    'webpixel' : os.path.join(font_folder, "webpixel bitmap_light.otf"),
    'agency' : os.path.join(font_folder, "AGENCYB.TTF"),
    'game_over': os.path.join(font_folder, "game_over.ttf"),
    'potra' : os.path.join(font_folder, "Potra.ttf")
    }

font_typo = {0: (font_array['webpixel'],60), 
             1:(font_array['webpixel'],30), 
             2:(font_array['game_over'],148),
             3:(font_array['game_over'],48),
}
font_color = {0: (black, white),
              1: (white, None),
              2: ((50,50,50),None),
              3: (black, None),
              4: ((200,0,0), None),
              5: ((1,1,1),None),
              6: (blue,None)}


def textdisplay(message, color, fontset):
    font = pygame.font.Font(fontset[0],fontset[1])
    text = font.render(message, True, color[0], color[1])
    textRect = text.get_rect()
    
    return text,textRect

music_folder = os.path.join(game_folder, 'music') 

music_array = {
    'main_menu': os.path.join(music_folder, "title_screen.mp3"),
    'main_game': os.path.join(music_folder, "main_game.mp3"),
    }

beep_array = {
    'beep01' : pygame.mixer.Sound(os.path.join(music_folder, "Powerup2.wav")) ,#Hit
    'beep02' : pygame.mixer.Sound(os.path.join(music_folder, "Powerup4.wav")) ,#Potion
    'beep03' : pygame.mixer.Sound(os.path.join(music_folder, "Pickup_Coin8.wav")) ,#Potion
    }

def playmusic(music,repeat = 0,start_at = 0.0): 
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(repeat,start_at)
    
def stopmusic():
    pygame.mixer.music.stop()
