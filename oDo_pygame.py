"""
RoboTetropolis
Created on 2012-01-23
@author: Xenmen
"""

# Rect.clip(bounding Rect)
 

import platform
import pygame, random, time

screen = pygame.Surface((640, 480))
background = pygame.Surface((640, 480))
clock = pygame.time.Clock() # create clock object
playing = False
playmusic = True
playing_music = False
first_play_music = True
songs = []
gameover = False
bounds = pygame.Rect(0, 0, 4, 4)

blocknames = ["block_blue_dark", "block_blue_lite", "block_brown", "block_green", "block_grey", "block_purple", "block_red", "block_yellow", "block_ROBO"]
#blocknames = ["robo"]
max_tower_height = 0
block_field = pygame.Rect(0, 0, 4, 4)
block_cur = pygame.Rect(0, 0, 4, 4)
block_next = pygame.Rect(0, 0, 4, 4)
block_tower = pygame.Rect(0, 0, 4, 4)
colours, img_blocks = [], []


def path_fix(name, path="Resources"):
	#with 'platform':
	if platform.system() == "Linux": return ("%s\/" %(path)) + name
	elif platform.system() == "Windows": return ("%s\\" %(path)) + name
	#without 'platform':
	#return ("%s\\" %(path)) + name

def load_image(name):
	return pygame.image.load(path_fix(name)).convert()

def load_song(name):
	global songs
	songs.append(path_fix(name))

def initialize(x, y, back_image_name):
	global screen, background, bounds, clock
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()
	full_screen = True
	if full_screen:
		screen = pygame.display.set_mode([x,y], pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode([x,y])
	screen.fill([255,255,255])
	pygame.display.set_caption("press Esc to quit. FPS: %.2f" % (clock.get_fps()))
	background = load_image(back_image_name)
	bounds = background.get_rect()

def blit_to_screen(surface, coords):
	global screen
	screen.blit(surface, coords)

def draw_square(colour, x, y, w=5, h=5):
	global screen
	screen.fill(colour, pygame.Rect(x, y, w, h))

def blank_screen():
	global screen
	screen.fill((255,255,255))

def save_screencap():
	global screen
	save_image(screen, ("screencap_-_%s.png" %time.strftime("%Y-%m-%d %H;%M;%S %Z", time.localtime(time.time()))))

def save_image(Surface, filename):
	pygame.image.save(Surface, path_fix(filename, "Saves"))

def music_load(song_num):
	global songs, playing_music, first_play_music
	pygame.mixer.music.load(songs[song_num])
	first_play_music = True

def music_bool(song_num=0):
	global playing_music, first_play_music
	if playing_music:
		pygame.mixer.music.pause()
		playing_music = False
	else:
		if first_play_music:
			music_load(song_num)
			pygame.mixer.music.play(-1)
			first_play_music = False
			playing_music = True
		else:
			pygame.mixer.music.unpause()
			playing_music = True

def music_switch(song_num):
	music_stop()
	music_bool(song_num)

def music_stop():
	global playing_music, first_play_music
	pygame.mixer.music.stop()
	playing_music = False
	first_play_music = True
