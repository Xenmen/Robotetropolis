"""
RoboTetropolis
Created on 2012-01-23
@author: Xenmen
Copyright: Daniel tadeuszow

    This file is part of Robotetropolis.

    Robotetropolis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Robotetropolis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Robotetropolis.  If not, see <http://www.gnu.org/licenses/>.
"""

# Rect.clip(bounding Rect)
 

import platform
import pygame, random, Queue, time
import oDo_pygame



def initialize_Tetris():
	oDo_pygame.initialize(640, 480, "game_playfield.PNG")
	oDo_pygame.load_song("game_tetris.mp3")
	oDo_pygame.load_song("game_tetris_lose.mp3")
	oDo_pygame.img_blocks = []
	#
	# LOAD ADDITIONAL RESOURCES
	#
	# Load Blocks
	for name in oDo_pygame.blocknames:
		if platform.system() == "Linux": oDo_pygame.img_blocks.append(oDo_pygame.load_image("blocks\/%s.PNG" %name))
		elif platform.system() == "Windows": oDo_pygame.img_blocks.append(oDo_pygame.load_image("blocks\\%s.PNG" %name))
	
	oDo_pygame.colours = oDo_pygame.img_blocks.__len__()
	#
	oDo_pygame.block_field_rect = pygame.Rect(12, 16, 384, oDo_pygame.bounds.h - 32)
	oDo_pygame.block_field = oDo_pygame.screen.subsurface(oDo_pygame.block_field_rect)
	# Prepare block things
	oDo_pygame.max_tower_height = oDo_pygame.block_field_rect.h
	reset()
	# Show funky preview thing
	opening_Tetris()

def load_frame_anim(img_name, folder):
	return oDo_pygame.load_image(oDo_pygame.path_fix(img_name, folder))

def opening_Tetris():		# A spiffy intro animation implemented
	time_to_build = pygame.mixer.Sound(oDo_pygame.path_fix("anim_intro\\time.ogg"))
	preview = oDo_pygame.load_image("game_preview.PNG")
	oDo_pygame.screen.blit(preview, (0,0))
	pygame.display.update()
	#print "Mixer init is:", pygame.mixer.get_init()
	
	# "Time to build Robotropolis" loop
	intro_anim_rect = pygame.Rect(345, 95, 170, 130)
	
	norm = load_frame_anim("anim_norm.PNG", "anim_intro")
	buh = load_frame_anim("anim_Buh.PNG", "anim_intro")
	tuh = load_frame_anim("anim_Tuh.PNG", "anim_intro")
	tie = load_frame_anim("anim_Tie.PNG", "anim_intro")
	ooo = load_frame_anim("anim_Ooo.PNG", "anim_intro")
	mmm = load_frame_anim("anim_Mmm.PNG", "anim_intro")
	frames = [norm, buh, mmm, ooo, tie, tuh]
	anim = [[0, 0.2], [4, 0.2], [0, 0.2], [5, 0.1], [4, 0.2], [2, 0.1], [5, 0.1], [3, 0.3], [1, 0.1], [0, 0.1], [4, 0.1], [3, 0.1], [1, 0.1], [3, 0.1], [5, 0.1], [4, 0.1], [0, 0.1], [0, 0.5],]
	
	time.sleep(3)
	time_to_build.play()
	for step in anim:
		oDo_pygame.screen.blit(frames[step[0]], intro_anim_rect)
		pygame.display.update()
		time.sleep(step[1])
	time.sleep(1)

class tetris_Block:
	def __init__(self, myrect, colour=0):
		self.rect = myrect
		self.colour_index = colour
	def set_colour(self, colour):
		self.colour_index = colour

class tetris_Formation:
	# FAST FOOD FAST FOOD
	def __init__(self, starting_x, starting_y, width, height, row_size_limit, max_tower_height):
		self.start_x = starting_x
		self.start_y = starting_y
		self.rect = pygame.Rect(starting_x, starting_y, 0, 0)
		self.img_width = width
		self.img_height = height
		self.buffer_x = 0
		self.buffer_y = 0
		self.blocks = []
		self.max_tower_height = max_tower_height
		self.row_size_limit = row_size_limit
		self.row_sizes = []
		self.max_rows = max_tower_height/height
		for i in range(self.max_rows):
			self.row_sizes.append(0)
		self.new_block_rects = []
	def initialize(self):
		self.rect = pygame.Rect(self.start_x,self.start_y,0,0)
		self.blocks = []
	def random(self):
		self.initialize()
		newcolour = random.randrange(0, oDo_pygame.colours)
		
		xs = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, -1], [0, 0, 1, 1], [0, -1, 0, 1], [0, -1, 0, 1], [0, 0, -1, 1]]
		ys = [[2, 0, 1, 3], [1, 0, 2, 2], [1, 0, 2,  2], [1, 0, 1, 0], [1,  0, 0, 1], [1,  1, 0, 0], [0, 1,  0, 0]]
		index = random.randrange(0, xs.__len__())
		x = xs[index]
		y = ys[index]
		for i in range(xs[index].__len__()):
			newrect = pygame.Rect(self.start_x + (x[i] * self.img_width) + (x[i] * self.buffer_x),
									self.start_y + (y[i] * self.img_height) + (y[i] * self.buffer_y),
									self.img_width, self.img_height)
			newblock = tetris_Block(newrect, newcolour)
			self.blocks.append(newblock)
		self.eval_size()
	def move(self, x, y):
		self.rect.move_ip(x, y)
		for i in range(self.blocks.__len__()):
			self.blocks[i].rect.move_ip(x,y)
	def absorb(self, other_formation):
		self.new_block_rects = []
		for block in other_formation.blocks:
			self.blocks.append(block)
			self.new_block_rects.append(block.rect)
			self.update_row_size(block.rect)
		# ::Probably should be a temp fix only::
		full_row = self.full_row_check()
		while full_row != -1:
			self.remove_row(full_row)
			full_row = self.full_row_check()
	def get_blocks(self, other_formation):
		self.new_block_rects = []
		dif_x = self.rect.x - other_formation.rect.x
		dif_y = self.rect.y - other_formation.rect.y
		for block in other_formation.blocks:
			block.rect.move_ip(dif_x, dif_y)
			self.blocks.append(block)
			self.new_block_rects.append(block.rect)
			self.update_row_size(block.rect)
		#self.full_row_check()
	def update_row_size(self, block_rect):
		index = self.max_rows - (block_rect.y/self.img_height) - 1
		self.row_sizes[index] += 1
	def full_row_check(self):
		for i in range(self.row_sizes.__len__()):
			if self.row_sizes[i] >= self.row_size_limit: return i
		return -1
	def remove_row(self, row_index):
		block_num = self.blocks.__len__()
		for block_index in range(block_num):
			a = self.blocks[block_num - block_index - 1].rect.y
			b = self.max_tower_height - (self.img_height * (row_index + 1))
			#print a, b
			if a == b:
				self.blocks.pop(block_num - block_index - 1)
			elif self.blocks[block_num - block_index - 1].rect.y < self.max_tower_height - (self.img_height * (row_index + 1)):
				self.blocks[block_num - block_index - 1].rect.move_ip(0, self.img_height)
		for i in range(self.max_rows - row_index - 1):
			self.row_sizes[i + row_index] = self.row_sizes[i + row_index + 1]
		self.row_sizes[self.max_rows - 1] = 0
	def eval_size(self):
		self.rect = self.blocks[0].rect.unionall(self.blocks)
	def pop_block(self, block_index):
		self.blocks.pop(block_index)
		self.eval_size()
	def kill_block(self, block_rect):
		self.blocks.remove(block_rect)
		self.eval_size()

def run_Tetris():
	global screen, background, playing, gameover, playmusic
	global block_field, block_cur, block_next, block_tower, timestep, colours, img_blocks
	global img_block_blue_dark, img_block_blue_lite, img_block_brown, img_block_green, img_block_grey, img_block_purple, img_block_red, img_block_yellow
	oDo_pygame.screen.blit(oDo_pygame.background, (0,0))
	oDo_pygame.playing = True
	try:
		oDo_pygame.music_load(0)
	except:
		oDo_pygame.playmusic = False
	if oDo_pygame.playmusic:
		oDo_pygame.music_bool()
	pygame.time.set_timer(pygame.USEREVENT + 1, 800)
	pygame.event.clear()
	while oDo_pygame.playing:
		
		
		#
		# EVENT HANDLING
		#
		events = pygame.event.get()
		if events != None:
			events_Tetris(events)
		
		
		
		#
		# RENDER TIME
		#
		# Caption
		pygame.display.set_caption("Robotetropolis\t\t\tFPS: %.2f" % (oDo_pygame.clock.get_fps()))
		# Background render
		oDo_pygame.screen.blit(oDo_pygame.background, (0,0))
		#
		# Block field updating
		#
		# Tower render
		for block in oDo_pygame.block_tower.blocks:
			oDo_pygame.block_field.blit(oDo_pygame.img_blocks[block.colour_index], (block.rect.x, block.rect.y))
		# Current Block render
		for block in oDo_pygame.block_cur.blocks:
			oDo_pygame.block_field.blit(oDo_pygame.img_blocks[block.colour_index], (block.rect.x, block.rect.y))
		# Next Block render
		for block in oDo_pygame.block_next.blocks:
			oDo_pygame.screen.blit(oDo_pygame.img_blocks[block.colour_index], (block.rect.x, block.rect.y))
		# Gameover check
		if oDo_pygame.gameover:
			lose_screen = oDo_pygame.load_image("game_lose.PNG")
			oDo_pygame.screen.blit(lose_screen, (0,0))
			pygame.display.update()
			if oDo_pygame.playmusic:
				oDo_pygame.music_stop()
			#	print "Play gameover"
			#	
			gameover_Tetris()
		# Screen update
		pygame.display.update()

def gameover_Tetris():
	time_to_snoop = pygame.mixer.Sound(oDo_pygame.path_fix("anim_lose\\snooping.ogg"))
	time_to_snoop.play()
	pingas = True
	while pingas:
		myevents = pygame.event.get()
		for event in myevents:
			if event.type == pygame.QUIT:
				pingas = False
				oDo_pygame.playing = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pingas = False
					oDo_pygame.playing = False
				if event.key == pygame.K_SPACE:
					oDo_pygame.gameover = False
					pingas = False
					oDo_pygame.playing = True
					reset()
					if oDo_pygame.playmusic:
						oDo_pygame.music_bool(0)
	#time_to_snoop.stop()

def reset():
	global block_field, max_tower_height, block_cur, block_next, block_tower, img_blocks
	max_rows = oDo_pygame.block_field.get_rect().w/oDo_pygame.img_blocks[0].get_rect().w
	oDo_pygame.block_tower = tetris_Formation(0, 576, oDo_pygame.img_blocks[0].get_rect().w, oDo_pygame.img_blocks[0].get_rect().h, max_rows, oDo_pygame.max_tower_height)
	oDo_pygame.block_cur = tetris_Formation(160, 0, oDo_pygame.img_blocks[0].get_rect().w, oDo_pygame.img_blocks[0].get_rect().h, max_rows, oDo_pygame.max_tower_height)
	oDo_pygame.block_cur.random()
	oDo_pygame.block_next = tetris_Formation(452, 140, oDo_pygame.img_blocks[0].get_rect().w, oDo_pygame.img_blocks[0].get_rect().h, max_rows, oDo_pygame.max_tower_height)
	oDo_pygame.block_next.random()

def move_curblock(x, y):
	invalid = False
	oDo_pygame.bounds = oDo_pygame.block_field.get_rect()
	for block in oDo_pygame.block_cur.blocks:
	#for block_index in range(oDo_pygame.block_cur.blocks.__len__()):
		temp = block.rect.move(x, y)
		invalid = rect_tower_collide(temp)
		if not oDo_pygame.bounds.contains(temp):
			invalid = True
		if invalid: break
	if not invalid:
		oDo_pygame.block_cur.move(x, y)
	return invalid

def rotate_curblock(turn_right):
	# WIP WIP WIP WIP WIP WIP WIP
	bounds = oDo_pygame.block_field.get_rect()
	new_blocks = oDo_pygame.block_cur.blocks
	invalid = False
	for block_index in range(oDo_pygame.block_cur.blocks.__len__() - 1):
		newblock = oDo_pygame.block_cur.blocks[block_index + 1]
		dif_x = newblock.rect.x - new_blocks[0].rect.x
		dif_y = newblock.rect.y - new_blocks[0].rect.y
		
		block = pygame.Rect(newblock.rect.move(-dif_x, -dif_y))
		if turn_right:
			block.move_ip(dif_y, -dif_x)
		else:	# Turn left
			block.move_ip(-dif_y, dif_x)
		if rect_tower_collide(block):
			#print "Tower collide"
			invalid = True
		if not bounds.contains(block):
			#print "out of bounds"
			invalid = True
		if invalid: break
	if not invalid:
		for block_index in range(oDo_pygame.block_cur.blocks.__len__() - 1):
			dif_x = oDo_pygame.block_cur.blocks[block_index + 1].rect.x - oDo_pygame.block_cur.blocks[0].rect.x
			dif_y = oDo_pygame.block_cur.blocks[block_index + 1].rect.y - oDo_pygame.block_cur.blocks[0].rect.y
			
			oDo_pygame.block_cur.blocks[block_index + 1].rect.move_ip(-dif_x, -dif_y)
			if turn_right:
				oDo_pygame.block_cur.blocks[block_index + 1].rect.move_ip(dif_y, -dif_x)
			else:	# Turn left
				oDo_pygame.block_cur.blocks[block_index + 1].rect.move_ip(-dif_y, dif_x)

def rect_tower_collide(the_rect):
	for tower_block in oDo_pygame.block_tower.blocks:
		collisions = the_rect.colliderect(tower_block.rect)
		if collisions:
			#print "TOWER COLLISION!"
			return True
	return False

def move_curblock_drop():
	for i in range(oDo_pygame.block_cur.max_rows):
		if move_curblock(0, oDo_pygame.block_cur.img_height): return

def tower_hit():
	oDo_pygame.block_tower.absorb(oDo_pygame.block_cur)
	oDo_pygame.block_cur.initialize()
	oDo_pygame.block_cur.get_blocks(oDo_pygame.block_next)
	oDo_pygame.block_next.random()
	for block in oDo_pygame.block_cur.blocks:
		if rect_tower_collide(block.rect):
			oDo_pygame.gameover = True

def events_Tetris(myevents):
	for event in myevents:
		if event.type == pygame.QUIT:
			oDo_pygame.playing = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				oDo_pygame.playing = False
				
			elif event.key == pygame.K_LEFT:
				move_curblock(- oDo_pygame.block_cur.img_width, 0)
				
			elif event.key == pygame.K_RIGHT:
				move_curblock(oDo_pygame.block_cur.img_width, 0)
				
			elif event.key == pygame.K_DOWN:
				if move_curblock(0, oDo_pygame.block_cur.img_height):
					tower_hit()
				
			elif event.key == pygame.K_LALT or event.key == pygame.K_LCTRL:
				rotate_curblock(False)
				
			elif event.key == pygame.K_RALT or event.key == pygame.K_RCTRL:
				rotate_curblock(True)
				
			elif event.key == pygame.K_SPACE:
				move_curblock_drop()
				tower_hit()
				
		#elif event.type == pygame.KEYUP:
		#	pass
		#elif event.type == pygame.MOUSEMOTION:
		#	pass
		elif event.type == pygame.USEREVENT + 1:
			if move_curblock(0, oDo_pygame.block_cur.img_height):
				tower_hit()
		#else:
		#	pass
		#	print "unrecognized event:", event.type, pygame.event.event_name(event.type)

if __name__ == '__main__':
	initialize_Tetris()
	run_Tetris()
