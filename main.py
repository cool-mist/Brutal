import pygame
import os
import random

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Project Properties
gameName = "Brutal"
WIDTH = 640 
HEIGHT = 480
windowSize = (WIDTH,HEIGHT)
fps = 60

# Assets folder
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder,"img")
soundFolder = os.path.join(gameFolder,"sounds")

# Initialize
pygame.init()
pygame.mixer.init()
gameDisplay = pygame.display.set_mode(windowSize)
pygame.display.set_caption(gameName)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Load game graphics
background = pygame.image.load(os.path.join(imgFolder,'background.jpg')).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(os.path.join(imgFolder,"bullet_p.png")).convert()
mob_img = pygame.image.load(os.path.join(imgFolder,"mob.png")).convert()
player_img_1 = pygame.image.load(os.path.join(imgFolder,"player_1.png")).convert()
player_img_2 = pygame.image.load(os.path.join(imgFolder,"player_2.png")).convert()
player_img_3 = pygame.image.load(os.path.join(imgFolder,"player_3.png")).convert()
player_img_4 = pygame.image.load(os.path.join(imgFolder,"player_4.png")).convert()
player_anim = [player_img_1,player_img_2,player_img_3,player_img_4]


# Load game0 sounds
shoot_sound = pygame.mixer.Sound(os.path.join(soundFolder,'Laser_Shoot3.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join(soundFolder,'Explosion3.wav'))

# Bg Music
pygame.mixer.music.load(os.path.join(soundFolder,'spaceranger3.wav'))
pygame.mixer.music.set_volume(1)
explosion_sound.set_volume(0.1)
shoot_sound.set_volume(0.3)

# Helper functions
font_name = pygame.font.match_font('Times')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text,True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.center = (x,y)
	gameDisplay.blit(text_surface,text_rect)



# Class Definitions
class Player(pygame.sprite.Sprite):
	# player sprite
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.animState = 0
		self.timer = 0
		self.image = pygame.transform.scale(player_anim[self.animState-1], (50, 50)) 
		self.rect = self.image.get_rect()
		self.image.set_colorkey(WHITE)
		self.rect.center = (WIDTH / 2,HEIGHT - 30)
		self.speedx = 0

		

	def update(self):
		self.timer +=1
		if self.timer % 10 == 0:
			self.timer = 0 ;
			self.animState += 1
			self.animState %= 4
		
		self.image = pygame.transform.scale(player_anim[self.animState], (50, 50))
		self.image.set_colorkey(WHITE)
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speedx -= 10
		if keystate[pygame.K_d]:
			self.speedx += 10

		self.rect.x += self.speedx

		# Check for out of bounds 
		if self.rect.right > WIDTH or self.rect.left < 0:
			# Rollback the changes
			self.rect.x -= self.speedx
	def shoot(self):
		shoot_sound.play()
		b = Bullet(self.rect.center[0],self.rect.top)
		all_sprites.add(b)
		bullets.add(b)



class Mob(pygame.sprite.Sprite):
	# mob sprite
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(mob_img, (40, 40)) 
		self.rect = self.image.get_rect()
		self.image.set_colorkey(WHITE)
		self.rect.center = (random.randrange(self.rect.width,WIDTH - self.rect.width),random.randrange(-100,-10))
		self.speedx = random.randrange(-5,5)
		self.speedy = random.randrange(3,7)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx

		# Check left right OOB
		if self.rect.left < 0 or self.rect.right > WIDTH:
			self.speedx = -self.speedx
		# Check for out of bounds 
		if self.rect.bottom > WIDTH - 20:

			# Reinit
			self.rect.center = (random.randrange(self.rect.width,WIDTH - self.rect.width),random.randrange(-100,-10))
			self.speedy = random.randrange(3,7)
			self.speedx = random.randrange(-5,5)
	


class Bullet(pygame.sprite.Sprite):
	#Bullet Sprite. One for enemy and one for player
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)		
		self.image = pygame.transform.scale(bullet_img, (10, 20)) 
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.rect.bottom = y
		self.rect.left = x 
		self.speedy = -10

	def update(self):
		self.rect.bottom += self.speedy
		if self.rect.bottom < 0:
			self.kill()
		
def reinit():
	score = 0
	for mob in mobs:
		mob.kill()
	for i in range(5):
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)
		score = 0
		timeLeft = realTimeLeft * fps
player = Player()
score = 0
high = 0
realTimeLeft = 60
timeLeft = realTimeLeft*fps

mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

all_sprites.add(player)

for i in range(5):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

#Main Loop
gameEnd = False
gameOver = True
pygame.mixer.music.play(loops = -1)
while not gameEnd:
	#wait for fps

	clock.tick(fps);
	if not gameOver:
		timeLeft -= 1

	#Handle Events

	for event in pygame.event.get():

		# Quit event
		if event.type == pygame.QUIT:
			gameEnd = True
			pass
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # LMB = 1
				if not gameOver:
					player.shoot()
			elif event.button == 3:  # RMB = 3
				if gameOver:
					gameEnd  = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and gameOver:
				gameOver = False
				reinit()
				
	# Update
	all_sprites.update()

	# Collisions
	# Player bullet with mob
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		explosion_sound.play()
		score += 1
		high = max(high,score)
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)

	#Player with mob -> Gameends
	hits = pygame.sprite.spritecollide(player, mobs, True)
	
	if hits:
		gameOver = True
		timeLeft = realTimeLeft * fps
		for hit in hits:
			m = Mob()
			all_sprites.add(m)
			mobs.add(m)
	# Draw
	
	gameDisplay.fill(BLACK)
	gameDisplay.blit(background, background_rect)
	draw_text(gameDisplay, "LMB to shoot", 20, WIDTH-100,HEIGHT-30)
	draw_text(gameDisplay, "Time Left :"+str(round(timeLeft/fps,1)), 20, 80,HEIGHT-30)	
	draw_text(gameDisplay, "HI: "+str(high)+"        SCORE: "+str(score), 20, WIDTH/2, 20)
	if not gameOver:
		all_sprites.draw(gameDisplay)

	# Update display after drawing everything
	if gameOver:
		draw_text(gameDisplay, "SPACE to Start, RMB to Quit",20,WIDTH / 2, HEIGHT / 2)
	
	pygame.display.update()
	
	
pygame.quit()
quit()