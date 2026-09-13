from pygame import *
init()
from random import *
from button import Button
from math import *
import asyncio
screen = display.set_mode((1280, 720))
display.set_caption('Cake or Die')
screen.fill((0, 0, 0)) 
icono = image.load("cakeordie_images/icono_cakeordie.png")
display.set_icon(icono)

class Objeto(sprite.Sprite):
	def __init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team):
		sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.ancho = ancho
		self.largo = largo
		self.direccionx = direccionx
		self.direcciony = direcciony
		self.puntuacion = puntuacion
		self.color = color
		self.vidas = vidas
		self.team = team

	def DibujarObjeto(self):
		draw.rect(screen, self.color, (self.x,self.y,self.ancho,self.largo))

	def check_colisiones(sprite1, sprite2):
		xsprite1 = sprite1.x
		ysprite1 = sprite1.y
		anchosprite1 = sprite1.ancho
		largosprite1 = sprite1.largo
		xsprite2 = sprite2.x
		ysprite2 = sprite2.y
		anchosprite2 = sprite2.ancho
		largosprite2 = sprite2.largo
		if (ysprite1 + largosprite1) > ysprite2 and ysprite1 < (ysprite2 + largosprite2) and (xsprite1 + anchosprite1) > xsprite2 and xsprite1 < (xsprite2 + anchosprite2):
			return True

class Bola(Objeto):
	def __init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team):
		Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team)
	
	def Movimiento(self):
		global salto, angulo, x_jump, salto_doble, w, correr, suelo, x_sup, jump, quieto
		x = self.x
		y = self.y
		keys = key.get_pressed()
		if angulo == 0.0 and suelo == False:
			self.y += 4
		else:
			if suelo == True:
				salto = False
				angulo = 0.0
				x_jump = self.y
				x_sup = self.y
				salto_doble = True
			if keys[K_w]==1 and angulo == 0.0:
				angulo = 0.001
				salto = True
				w = True
			if keys[K_w]==0:
				w = False
			if keys[K_w]==1 and w == False and salto_doble == False:
				angulo = 0.001
				x_jump = self.y
				salto_doble = True
			
			if salto == True:
				jump += 1
				if jump == 50:
					jump = 0
					x_jump = x_sup
					salto_doble = False
					salto = False
			if angulo == 0.0 and suelo == False and x_jump != x_sup:
				x_jump = x_sup
				angulo = pi / 2

			self.y = x_jump - sin(angulo)*100
			
			if 0 < angulo:
				angulo += 0.05
			if angulo > pi:
				angulo = 0.0

		if keys[K_w]:
			self.direcciony = 1

		if keys[K_s]:
			self.direcciony = 0
		
		if keys[K_a]:
			self.direccionx = 0
			self.direcciony = 2
			correr = True
			if x > 0:
				self.x -= 5
		if keys[K_d]:
			self.direccionx = 1
			self.direcciony = 2
			correr = True
			if x < 1260:
				self.x += 5
		if keys[K_a] == 0 and keys[K_d] == 0:
			correr = False
		if self.y >= 569:
			self.y = 569
			suelo = True
			angulo = 0.0
			salto = False
			salto_doble = True
			jump = 0
    
	def check_suelo(self, sprite1):
		if (sprite1.y + sprite1.largo) >= self.y and sprite1.y <= (self.y + self.largo) and (sprite1.x + sprite1.ancho) > self.x and sprite1.x < (self.x + self.ancho):
			return True
    
	def MovimientoLemon(self, plataforma):
		if self.check_colisiones(plataforma) == True:
			damage_sound.play()
			plataforma.vidas -= 1
			self.x = 1280
			self.y = 210
		if self.direccionx == 0:
			self.x -= 2
		if self.direccionx == 1:
			self.x += 2
		if self.direcciony == 0:
			self.y -= 5
		if self.direcciony == 1:
			self.y += 5
		if self.x <= 0 and self.direccionx == 0:
			self.x = 1260
		if self.x >= 1280 and self.direccionx == 1:
			self.x = 0
		if self.y <= 0:
			lemon_sound.play()
			self.direcciony = 1
		if self.y >= 599:
			lemon_sound.play()
			self.direcciony = 0
    
	def MovimientoGelatina(self, plataforma):
		if self.check_colisiones(plataforma) == True:
			damage_sound.play()
			plataforma.vidas -= 1
			self.x = 1280
			self.y = 100
		if self.direccionx == 0:
			self.x -= 1
		if self.direccionx == 1:
			self.x += 1
		if self.direcciony == 0:
			if self.y <= 100: self.y -= 0.625
			elif self.y <= 200: self.y -= 2.5
			elif self.y <= 400: self.y -= 5
			else: self.y -= 10
		if self.direcciony == 1:
			if self.y <= 100: self.y += 0.625
			elif self.y <= 200: self.y += 2.5
			elif self.y <= 400: self.y += 5
			else: self.y += 10
		if self.x <= 0 and self.direccionx == 0:
			self.x = 1260
			self.y = 100
		if self.x >= 1280 and self.direccionx == 1:
			self.x = 0
			self.y = 100
		if self.y <= 100:
			self.direcciony = 1
		if self.y >= 599:
			gelatina_sound.play()
			self.direcciony = 0
    
	def MovimientoTortitas(self, plataforma):
		if self.check_colisiones(plataforma) == True:
			damage_sound.play()
			plataforma.vidas -= 1
			self.x = 1280
		if self.direccionx == 0:
			self.x -= 5
		if self.direccionx == 1:
			self.x += 5
		if self.x <= -1000 and self.direccionx == 0:
			tortita_sound.play()
			self.x = 1260
		if self.x >= 2280 and self.direccionx == 1:
			tortita_sound.play()
			self.x = 0
    
	def MovimientoDonut(self, plataforma):
		if self.check_colisiones(plataforma):
			damage_sound.play()
			plataforma.vidas -= 1
			self.y = -100
		if self.y < 600:
			if self.y == -100:
				self.x = randrange(1, 13) * 100
			self.y += 4
		if self.y >= 600:
			donut_sound.play()
			self.y = -100

	def MovimientoHuevo(self, plataforma):
		global puntuacion_minijuegos
		if self.direcciony == 1:
			if self.y < 720:
				if self.y == -100:
					self.x = randrange(1, 13) * 100
				self.y += 4
			if self.y >= 720:
				self.y = -100
		elif self.direccionx == 1:
			if self.x < 1280:
				if self.x == -100:
					self.y = randrange(1, 7) * 100
				self.x += 4
			if self.x >= 1280:
				self.x = -100

def barra_tiempo(screen, x, y, hp, color):
	largo = 165
	ancho = 20
	calculo_barra = int((hp / 100)*largo)
	draw.rect(screen, color, Rect(x, y, calculo_barra, ancho))

def barajar_cartas():
	global posiciones
	for y in [250, 500]:
		for x in [100, 300, 500, 700, 900, 1100]:
			posiciones.append((x, y))
	shuffle(posiciones)

def get_font(size):
    return font.Font("menu_assets/font.ttf", size)

clock = time.Clock()
fondo = transform.scale(image.load("cakeordie_images/fondo.png").convert(), (1280, 720))
pinky1 = transform.scale(image.load("cakeordie_images/pinky1.png"), (40, 40))
pinky2 = transform.scale(image.load("cakeordie_images/pinky2.png"), (40, 40))
pinky_run11 = transform.scale(image.load("cakeordie_images/pinky_run11.png"), (40, 40))
pinky_run21 = transform.scale(image.load("cakeordie_images/pinky_run21.png"), (40, 40))
pinky_run12 = transform.scale(image.load("cakeordie_images/pinky_run12.png"), (40, 40))
pinky_run22 = transform.scale(image.load("cakeordie_images/pinky_run22.png"), (40, 40))
pinky_jump1 = transform.scale(image.load("cakeordie_images/pinky_jump1.png"), (40, 40))
pinky_jump2 = transform.scale(image.load("cakeordie_images/pinky_jump2.png"), (40, 40))
cake = transform.scale(image.load("cakeordie_images/cake.png"), (200, 200))
cake1 = transform.scale(image.load("cakeordie_images/cake1.png"), (200, 200))
cake2 = transform.scale(image.load("cakeordie_images/cake2.png"), (200, 200))
cake3 = transform.scale(image.load("cakeordie_images/cake3.png"), (200, 200))
cake4 = transform.scale(image.load("cakeordie_images/cake4.png"), (200, 200))
cake5 = transform.scale(image.load("cakeordie_images/cake5.png"), (200, 200))
lemon1 = transform.scale(image.load("cakeordie_images/lemon1.png"), (32, 32))
lemon2 = transform.scale(image.load("cakeordie_images/lemon2.png"), (32, 32))
jelly = transform.scale(image.load("cakeordie_images/jelly.png"), (32, 32))
pancake = transform.scale(image.load("cakeordie_images/pancake.png"), (64, 64))
dona = transform.scale(image.load("cakeordie_images/dona.png"), (48, 48))
egg11 = transform.scale(image.load("cakeordie_images/egg11.png"), (64, 64))
egg21 = transform.scale(image.load("cakeordie_images/egg21.png"), (64, 64))
egg31 = transform.scale(image.load("cakeordie_images/egg31.png"), (64, 64))
egg41 = transform.scale(image.load("cakeordie_images/egg41.png"), (64, 64))
egg51 = transform.scale(image.load("cakeordie_images/egg51.png"), (64, 64))
egg12 = transform.scale(image.load("cakeordie_images/egg12.png"), (64, 64))
egg22 = transform.scale(image.load("cakeordie_images/egg22.png"), (64, 64))
egg32 = transform.scale(image.load("cakeordie_images/egg32.png"), (64, 64))
egg42 = transform.scale(image.load("cakeordie_images/egg42.png"), (64, 64))
egg52 = transform.scale(image.load("cakeordie_images/egg52.png"), (64, 64))
egg13 = transform.scale(image.load("cakeordie_images/egg13.png"), (64, 64))
egg23 = transform.scale(image.load("cakeordie_images/egg23.png"), (64, 64))
egg33 = transform.scale(image.load("cakeordie_images/egg33.png"), (64, 64))
egg43 = transform.scale(image.load("cakeordie_images/egg43.png"), (64, 64))
egg53 = transform.scale(image.load("cakeordie_images/egg53.png"), (64, 64))
egg14 = transform.scale(image.load("cakeordie_images/egg14.png"), (64, 64))
egg24 = transform.scale(image.load("cakeordie_images/egg24.png"), (64, 64))
egg34 = transform.scale(image.load("cakeordie_images/egg34.png"), (64, 64))
egg44 = transform.scale(image.load("cakeordie_images/egg44.png"), (64, 64))
egg54 = transform.scale(image.load("cakeordie_images/egg54.png"), (64, 64))
pair1 = transform.scale(image.load("cakeordie_images/pair1.png"), (128, 192))
pair2 = transform.scale(image.load("cakeordie_images/pair2.png"), (128, 192))
pair3 = transform.scale(image.load("cakeordie_images/pair3.png"), (128, 192))
pair4 = transform.scale(image.load("cakeordie_images/pair4.png"), (128, 192))
pair5 = transform.scale(image.load("cakeordie_images/pair5.png"), (128, 192))
pair6 = transform.scale(image.load("cakeordie_images/pair6.png"), (128, 192))
pair7 = transform.scale(image.load("cakeordie_images/pair7.png"), (128, 192))
boton = transform.scale(image.load("cakeordie_images/boton.png"), (128, 128))
b1 = transform.scale(image.load("cakeordie_images/1.png"), (32, 32))
b2 = transform.scale(image.load("cakeordie_images/2.png"), (32, 32))
b3 = transform.scale(image.load("cakeordie_images/3.png"), (32, 32))
b4 = transform.scale(image.load("cakeordie_images/4.png"), (32, 32))
b5 = transform.scale(image.load("cakeordie_images/5.png"), (32, 32))
b6 = transform.scale(image.load("cakeordie_images/6.png"), (32, 32))
b7 = transform.scale(image.load("cakeordie_images/7.png"), (32, 32))
b8 = transform.scale(image.load("cakeordie_images/8.png"), (32, 32))
b9 = transform.scale(image.load("cakeordie_images/9.png"), (32, 32))
b0 = transform.scale(image.load("cakeordie_images/0.png"), (32, 32))
bb = transform.scale(image.load("cakeordie_images/BORRAR.png"), (32, 32))
be = transform.scale(image.load("cakeordie_images/ENTER.png"), (32, 32))
trozo = transform.scale(image.load("cakeordie_images/trozo.png"), (64, 64))
trozo2 = transform.scale(image.load("cakeordie_images/trozo2.png"), (64, 64))
donut_sound = mixer.Sound('cakeordie_sounds/Gota.ogg')
donut_sound.set_volume(0.0625)
lemon_sound = mixer.Sound('cakeordie_sounds/Tornado.ogg')
lemon_sound.set_volume(0.0315)
gelatina_sound = mixer.Sound('cakeordie_sounds/Gelatina.ogg')
gelatina_sound.set_volume(0.125)
tortita_sound = mixer.Sound('cakeordie_sounds/Tortita.ogg')
tortita_sound.set_volume(0.25)
damage_sound = mixer.Sound('cakeordie_sounds/Damage.ogg')
damage_sound.set_volume(0.5)
win_sound = mixer.Sound('cakeordie_sounds/Win.ogg')
win_sound.set_volume(0.5)
win2_sound = mixer.Sound('cakeordie_sounds/Win2.ogg')
win2_sound.set_volume(0.5)
lose_sound = mixer.Sound('cakeordie_sounds/Lose.ogg')
lose_sound.set_volume(0.5)
lose2_sound = mixer.Sound('cakeordie_sounds/Lose2.ogg')
lose2_sound.set_volume(0.5)

async def main():
	global salto, angulo, x_jump, salto_doble, w, correr, suelo, x_sup, jump, quieto, puntuacion_minijuegos, pisos_tarta, posiciones
	salto = False
	angulo = 0.0
	x_jump = 575
	x_sup = 575
	salto_doble = False
	w = False
	correr = False
	suelo = False
	jump = 0
	quieto = True
	puntuacion_minijuegos = 0
	pisos_tarta = 1
	estado = "Menu"
	plataforma = Bola(640,599,15,30, 1, 1, 0, (0,0,255), 3, 0)
	enemigo = Bola(615,50,50,50, 1, 1, 0, (255,0,0), 100, 0)
	suelo1 = Bola(0, 599, 1280, 300, 1, 1, 0, (0, 0, 0), 0, 0)
	limon1 = Bola(0,0,15,15, 1, 1, 0, (0,255,0), 100, 0)
	limon2 = Bola(1280,0,15,15, 0, 1, 0, (0,255,0), 100, 0)
	limon3 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	limon4 = Bola(1280,600,15,15, 0, 1, 0, (0,255,0), 100, 0)
	limon5 = Bola(0,0,15,15, 1, 1, 0, (0,255,0), 100, 0)
	limon6 = Bola(1280,0,15,15, 0, 1, 0, (0,255,0), 100, 0)
	limon7 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	limon8 = Bola(1280,600,15,15, 0, 1, 0, (0,255,0), 100, 0)
	gelatina1 = Bola(0,100,15,15, 1, 1, 0, (0,255,0), 100, 0)
	gelatina2 = Bola(0,100,15,15, 1, 1, 0, (0,255,0), 100, 0)
	tortita1 = Bola(0,550,30,50, 1, 1, 0, (0,255,0), 100, 0)
	tortita2 = Bola(0,550,30,50, 0, 1, 0, (0,255,0), 100, 0)
	tortita3 = Bola(0,500,30,50, 1, 1, 0, (0,255,0), 100, 0)
	tortita4 = Bola(0,500,30,50, 0, 1, 0, (0,255,0), 100, 0)
	donut1 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	donut2 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	donut3 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	donut4 = Bola(0,600,15,15, 1, 1, 0, (0,255,0), 100, 0)
	animacion_run = 0
	tiempo_minijuego = 1000 #Minijuego1 = 750
	tiempo_juego = 0
	final_sound = False
	resultado_minijuego = False
	while True:
		if estado == "Menu":
			mixer.music.stop()
			screen.fill((0, 0, 0)) 

			MENU_MOUSE_POS = mouse.get_pos()

			MENU_TEXT = get_font(75).render("CAKE OR DIE", True, (244, 137, 246))
			MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

			PLAY_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 250), 
								text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			OPTIONS_BUTTON = Button(image=image.load("menu_assets/Options Rect.png"), pos=(640, 400), 
								text_input="OPTIONS", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			QUIT_BUTTON = Button(image=image.load("menu_assets/Quit Rect.png"), pos=(640, 550), 
								text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

			screen.blit(MENU_TEXT, MENU_RECT)

			for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
				button.changeColor(MENU_MOUSE_POS)
				button.update(screen)
			
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type == MOUSEBUTTONDOWN:
					if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
						mixer.music.set_volume(0.25)
						mixer.music.load('cakeordie_sounds/Musica.ogg')
						mixer.music.set_volume(mixer.music.get_volume())
						mixer.music.play(-1)
						estado = "Play"
					if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
						estado = "Options"
					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						quit()
						exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()
			display.update()
		
		elif estado == "Options":
			mixer.music.stop()
			OPTIONS_MOUSE_POS = mouse.get_pos()

			screen.fill((0, 0, 0)) 

			OPTIONS_TEXT = get_font(45).render("OPTIONS", True, (244, 137, 246))
			OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
			screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

			DECREASE_TEXT = get_font(45).render("1 : Decrease Volume", True, (215, 252, 212))
			DECREASE_RECT = DECREASE_TEXT.get_rect(center=(640, 250))
			screen.blit(DECREASE_TEXT, DECREASE_RECT)

			INCREASE_TEXT = get_font(45).render("2 : Increase Volume", True, (215, 252, 212))
			INCREASE_RECT = INCREASE_TEXT.get_rect(center=(640, 400))
			screen.blit(INCREASE_TEXT, INCREASE_RECT)

			OPTIONS_BACK = Button(image=None, pos=(640, 550), 
								text_input="BACK", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

			OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
			OPTIONS_BACK.update(screen)

			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type == MOUSEBUTTONDOWN:
					if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
						estado = "Menu"
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						estado = "Menu"

			display.update()
		
		elif estado == "Play":
			screen.blit(fondo, (0, 0))
			plataforma.Movimiento()

			tiempo_juego += 1

			if plataforma.vidas == 3:
				screen.blit(trozo, (10, 10))
				screen.blit(trozo, (70, 10))
				screen.blit(trozo, (130, 10))
			elif plataforma.vidas == 2:
				screen.blit(trozo, (10, 10))
				screen.blit(trozo, (60, 10))
				screen.blit(trozo2, (110, 10))
			elif plataforma.vidas == 1:
				screen.blit(trozo, (10, 10))
				screen.blit(trozo2, (60, 10))
				screen.blit(trozo2, (110, 10))
			elif plataforma.vidas <= 0:
				if pisos_tarta > 1: pisos_tarta -= 1
				plataforma.vidas = 3

			if pisos_tarta == 1: screen.blit(cake1, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 2: screen.blit(cake2, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 3: screen.blit(cake3, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 4: screen.blit(cake4, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 5: screen.blit(cake5, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 6: screen.blit(cake, (enemigo.x-75, enemigo.y))

			#ANIMACIÓN LEMON
			limon1.MovimientoLemon(plataforma)
			limon2.MovimientoLemon(plataforma)
			if limon1.direccionx == 1:
			    screen.blit(lemon1, (limon1.x-10, limon1.y-10))
			else:
			    screen.blit(lemon2, (limon1.x-10, limon1.y-10))
			if limon2.direccionx == 1:
			    screen.blit(lemon1, (limon2.x-10, limon2.y-10))
			else:
			    screen.blit(lemon2, (limon2.x-10, limon2.y-10))
			
			if tiempo_juego >= 3000:
				limon3.MovimientoLemon(plataforma)
				limon4.MovimientoLemon(plataforma)
				if limon3.direccionx == 1:
					screen.blit(lemon1, (limon3.x-10, limon3.y-10))
				else:
					screen.blit(lemon2, (limon3.x-10, limon3.y-10))
				if limon4.direccionx == 1:
					screen.blit(lemon1, (limon4.x-10, limon4.y-10))
				else:
					screen.blit(lemon2, (limon4.x-10, limon4.y-10))
			
			if tiempo_juego >= 6000:
				limon5.MovimientoLemon(plataforma)
				limon6.MovimientoLemon(plataforma)
				if limon5.direccionx == 1:
					screen.blit(lemon1, (limon5.x-10, limon5.y-10))
				else:
					screen.blit(lemon2, (limon5.x-10, limon5.y-10))
				if limon6.direccionx == 1:
					screen.blit(lemon1, (limon6.x-10, limon6.y-10))
				else:
					screen.blit(lemon2, (limon6.x-10, limon6.y-10))

			if tiempo_juego >= 9000:
				limon7.MovimientoLemon(plataforma)
				limon8.MovimientoLemon(plataforma)
				if limon7.direccionx == 1:
					screen.blit(lemon1, (limon7.x-10, limon7.y-10))
				else:
					screen.blit(lemon2, (limon7.x-10, limon7.y-10))
				if limon8.direccionx == 1:
					screen.blit(lemon1, (limon8.x-10, limon8.y-10))
				else:
					screen.blit(lemon2, (limon8.x-10, limon8.y-10))
			
			#ANIMACIÓN GELATINA
			if tiempo_juego >= 750:
				gelatina1.MovimientoGelatina(plataforma)
				screen.blit(jelly, (gelatina1.x-10, gelatina1.y-10))

			if tiempo_juego >= 6000:
				gelatina2.MovimientoGelatina(plataforma)
				screen.blit(jelly, (gelatina2.x-10, gelatina2.y-10))
			
			#ANIMACIÓN TORTITA
			if tiempo_juego >= 1500:
				tortita1.MovimientoTortitas(plataforma)
				screen.blit(pancake, (tortita1.x-20, tortita1.y-5))

			if tiempo_juego >= 3000:
				tortita2.MovimientoTortitas(plataforma)
				screen.blit(pancake, (tortita2.x-20, tortita2.y-5))
			
			if tiempo_juego >= 9000:
				tortita3.MovimientoTortitas(plataforma)
				screen.blit(pancake, (tortita3.x-20, tortita3.y-5))
				tortita4.MovimientoTortitas(plataforma)
				screen.blit(pancake, (tortita4.x-20, tortita4.y-5))

			#ANIMACIÓN DONUT
			if tiempo_juego >= 2250:
				donut1.MovimientoDonut(plataforma)
				donut2.MovimientoDonut(plataforma)
				screen.blit(dona, (donut1.x-17.5, donut1.y-22.5))
				screen.blit(dona, (donut2.x-17.5, donut2.y-22.5))

			if tiempo_juego >= 6000:
				donut3.MovimientoDonut(plataforma)
				donut4.MovimientoDonut(plataforma)
				screen.blit(dona, (donut3.x-17.5, donut3.y-22.5))
				screen.blit(dona, (donut4.x-17.5, donut4.y-22.5))

			#ANIMACIÓN PINKY
			if suelo == False:
				if plataforma.direccionx == 1:
					screen.blit(pinky_jump1, (plataforma.x-11, plataforma.y-10))
				else:
					screen.blit(pinky_jump2, (plataforma.x-11, plataforma.y-10))
			else:
				if correr == True:
					animacion_run += 1
					if plataforma.direccionx == 1:
						if animacion_run <= 15:
							screen.blit(pinky_run11, (plataforma.x-11, plataforma.y-10))
						elif animacion_run <= 30:
							screen.blit(pinky_run12, (plataforma.x-11, plataforma.y-10))
					else:
						if animacion_run <= 15:
							screen.blit(pinky_run21, (plataforma.x-14, plataforma.y-10))
						elif animacion_run <= 30:
							screen.blit(pinky_run22, (plataforma.x-14, plataforma.y-10))
					if animacion_run > 30: animacion_run = 0
				else:
					if plataforma.direccionx == 1:
						screen.blit(pinky1, (plataforma.x-11, plataforma.y-10))
					else:
						screen.blit(pinky2, (plataforma.x-14, plataforma.y-10))

			#MINIJUEGOS
			if tiempo_juego == 3000:
				tiempo_minijuego = 750
				puntuacion_minijuegos = 0
				animacion_huevo = 0
				huevo1 = Bola(-100,0,40,40, 1, 0, 0, (255,0,0), 100, 0)
				huevo2 = Bola(-100,0,40,40, 1, 0, 0, (0,255,0), 100, 0)
				huevo3 = Bola(0,-100,40,40, 0, 1, 0, (255,0,0), 100, 0)
				huevo4 = Bola(0,-100,40,40, 0, 1, 0, (255,0,0), 100, 0)
				huevo5 = Bola(-100,0,40,40, 1, 0, 0, (255,0,0), 100, 0)
				huevo6 = Bola(-100,0,40,40, 1, 0, 0, (255,0,0), 100, 0)
				huevo7 = Bola(0,-100,40,40, 0, 1, 0, (255,0,0), 100, 0)
				huevo8 = Bola(0,-100,40,40, 0, 1, 0, (0,255,0), 100, 0)
				huevo9 = Bola(-100,0,40,40, 1, 0, 0, (255,0,0), 100, 0)
				huevo10 = Bola(0,-100,40,40, 0, 1, 0, (255,0,0), 100, 0)
				inicio_temporizador = time.get_ticks()
				tiempo_inicio = 0
				estado = "Minijuego1"
			if tiempo_juego == 6000:
				tiempo_minijuego = 1000
				puntuacion_minijuegos = 0
				posiciones = []
				barajar_cartas()
				pareja11 = Bola(posiciones[0][0],posiciones[0][1],40,40, 0, 1, 0, (255,0,0), 100, 0)
				pareja12 = Bola(posiciones[1][0],posiciones[1][1],40,40, 0, 1, 0, (255,0,0), 100, 0)
				pareja21 = Bola(posiciones[2][0],posiciones[2][1],40,40, 0, 1, 0, (0,255,0), 100, 0)
				pareja22 = Bola(posiciones[3][0],posiciones[3][1],40,40, 0, 1, 0, (0,255,0), 100, 0)
				pareja31 = Bola(posiciones[4][0],posiciones[4][1],40,40, 0, 1, 0, (0,0,255), 100, 0)
				pareja32 = Bola(posiciones[5][0],posiciones[5][1],40,40, 0, 1, 0, (0,0,255), 100, 0)
				pareja41 = Bola(posiciones[6][0],posiciones[6][1],40,40, 0, 1, 0, (125,0,0), 100, 0)
				pareja42 = Bola(posiciones[7][0],posiciones[7][1],40,40, 0, 1, 0, (125,0,0), 100, 0)
				pareja51 = Bola(posiciones[8][0],posiciones[8][1],40,40, 0, 1, 0, (0,125,0), 100, 0)
				pareja52 = Bola(posiciones[9][0],posiciones[9][1],40,40, 0, 1, 0, (0,125,0), 100, 0)
				pareja61 = Bola(posiciones[10][0],posiciones[10][1],40,40, 0, 1, 0, (0,0,125), 100, 0)
				pareja62 = Bola(posiciones[11][0],posiciones[11][1],40,40, 0, 1, 0, (0,0,125), 100, 0)
				pareja = 0
				pareja1= False
				pareja2= False
				pareja3= False
				pareja4= False
				pareja5= False
				pareja6= False
				inicio_temporizador = time.get_ticks()
				tiempo_inicio = 0
				estado = "Minijuego2"
			if tiempo_juego == 9000:
				tiempo_minijuego = 750
				eggs_bill = choice([6, 12, 18]) #3, 6, 9
				milk_bill = choice([1, 2, 3]) #2, 4, 6
				chocolate_bill = choice([4, 5, 6]) #12, 15, 18
				strawberry_bill = choice([10, 20, 30]) #2, 4, 6
				cheese_bill = choice([1, 2, 3]) #5, 10, 15
				cookie_bill = choice([7, 8, 9]) #7, 8, 9
				precio_bill = 0
				precio_final = int((eggs_bill * 0.5) + (milk_bill * 2) + (chocolate_bill * 3) + (strawberry_bill * 0.2) + (cheese_bill * 5) + (cookie_bill * 1))
				enter = False
				inicio_temporizador = time.get_ticks()
				tiempo_inicio = 0
				estado = "Minijuego4"
			if tiempo_juego == 12000:
				tiempo_minijuego = 0
				inicio_temporizador = time.get_ticks()
				pulsado = False
				estado = "Minijuego3"
			if tiempo_juego > 12000:
				estado = "Final"

			suelo1.DibujarObjeto()
			#COMPROBACION SUELO
			if suelo1.check_suelo(plataforma):
				suelo = True
			else:
				suelo = False

			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()

		if estado == "Minijuego1":
			if tiempo_minijuego >= 0 and puntuacion_minijuegos < 10:
				screen.fill((0, 0, 0)) 

				if tiempo_inicio > 1500:
					huevo1.MovimientoHuevo(plataforma)
					huevo2.MovimientoHuevo(plataforma)
					huevo3.MovimientoHuevo(plataforma)
					huevo4.MovimientoHuevo(plataforma)
					huevo5.MovimientoHuevo(plataforma)
					huevo6.MovimientoHuevo(plataforma)
					huevo7.MovimientoHuevo(plataforma)
					huevo8.MovimientoHuevo(plataforma)
					huevo9.MovimientoHuevo(plataforma)
					huevo10.MovimientoHuevo(plataforma)
					tiempo_minijuego -= 1
					animacion_huevo += 1

				if tiempo_minijuego >= 150: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 255, 255))
				else: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 0, 0))

				HUEVO_TEXT = get_font(37).render("PICK THE RAINBOW EGGS " + str(puntuacion_minijuegos) + "/10", True, (244, 137, 246))
				HUEVO_RECT = HUEVO_TEXT.get_rect(center=(640, 100))
				screen.blit(HUEVO_TEXT, HUEVO_RECT)

			if puntuacion_minijuegos == 10:
				screen.fill((0, 0, 0)) 
				HUEVO_TEXT = get_font(37).render("PICK THE RAINBOW EGGS " + str(puntuacion_minijuegos) + "/10", True, (244, 137, 246))
				HUEVO_RECT = HUEVO_TEXT.get_rect(center=(640, 100))
				screen.blit(HUEVO_TEXT, HUEVO_RECT)

			HUEVO_MOUSE_POS = mouse.get_pos()
			HUEVO1_BUTTON = Button(image=None, pos=(huevo1.x+25, huevo1.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			HUEVO2_BUTTON = Button(image=None, pos=(huevo2.x+25, huevo2.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			HUEVO3_BUTTON = Button(image=None, pos=(huevo3.x+25, huevo3.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))			
			HUEVO4_BUTTON = Button(image=None, pos=(huevo4.x+25, huevo4.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))			
			HUEVO5_BUTTON = Button(image=None, pos=(huevo5.x+25, huevo5.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))			
			HUEVO6_BUTTON = Button(image=None, pos=(huevo6.x+25, huevo6.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))			
			HUEVO7_BUTTON = Button(image=None, pos=(huevo7.x+25, huevo7.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))			
			HUEVO8_BUTTON = Button(image=None, pos=(huevo8.x+25, huevo8.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			HUEVO9_BUTTON = Button(image=None, pos=(huevo9.x+25, huevo9.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			HUEVO10_BUTTON = Button(image=None, pos=(huevo10.x+25, huevo10.y+25), text_input="H", font=get_font(37), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			
			if animacion_huevo <= 15:
				screen.blit(egg11, (huevo1.x-10, huevo1.y-10))
				screen.blit(egg21, (huevo2.x-10, huevo2.y-10))
				screen.blit(egg31, (huevo3.x-10, huevo3.y-10))
				screen.blit(egg41, (huevo4.x-10, huevo4.y-10))
				screen.blit(egg51, (huevo5.x-10, huevo5.y-10))
				screen.blit(egg41, (huevo6.x-10, huevo6.y-10))
				screen.blit(egg51, (huevo7.x-10, huevo7.y-10))
				screen.blit(egg21, (huevo8.x-10, huevo8.y-10))
				screen.blit(egg31, (huevo9.x-10, huevo9.y-10))
				screen.blit(egg11, (huevo10.x-10, huevo10.y-10))
			elif animacion_huevo <= 30:
				screen.blit(egg12, (huevo1.x-10, huevo1.y-10))
				screen.blit(egg22, (huevo2.x-10, huevo2.y-10))
				screen.blit(egg32, (huevo3.x-10, huevo3.y-10))
				screen.blit(egg42, (huevo4.x-10, huevo4.y-10))
				screen.blit(egg52, (huevo5.x-10, huevo5.y-10))
				screen.blit(egg42, (huevo6.x-10, huevo6.y-10))
				screen.blit(egg52, (huevo7.x-10, huevo7.y-10))
				screen.blit(egg22, (huevo8.x-10, huevo8.y-10))
				screen.blit(egg32, (huevo9.x-10, huevo9.y-10))
				screen.blit(egg12, (huevo10.x-10, huevo10.y-10))
			elif animacion_huevo <= 45:
				screen.blit(egg13, (huevo1.x-10, huevo1.y-10))
				screen.blit(egg23, (huevo2.x-10, huevo2.y-10))
				screen.blit(egg33, (huevo3.x-10, huevo3.y-10))
				screen.blit(egg43, (huevo4.x-10, huevo4.y-10))
				screen.blit(egg53, (huevo5.x-10, huevo5.y-10))
				screen.blit(egg43, (huevo6.x-10, huevo6.y-10))
				screen.blit(egg53, (huevo7.x-10, huevo7.y-10))
				screen.blit(egg23, (huevo8.x-10, huevo8.y-10))
				screen.blit(egg33, (huevo9.x-10, huevo9.y-10))
				screen.blit(egg13, (huevo10.x-10, huevo10.y-10))
			elif animacion_huevo <= 60:
				screen.blit(egg14, (huevo1.x-10, huevo1.y-10))
				screen.blit(egg24, (huevo2.x-10, huevo2.y-10))
				screen.blit(egg34, (huevo3.x-10, huevo3.y-10))
				screen.blit(egg44, (huevo4.x-10, huevo4.y-10))
				screen.blit(egg54, (huevo5.x-10, huevo5.y-10))
				screen.blit(egg44, (huevo6.x-10, huevo6.y-10))
				screen.blit(egg54, (huevo7.x-10, huevo7.y-10))
				screen.blit(egg24, (huevo8.x-10, huevo8.y-10))
				screen.blit(egg34, (huevo9.x-10, huevo9.y-10))
				screen.blit(egg14, (huevo10.x-10, huevo10.y-10))
				if animacion_huevo == 60: animacion_huevo = 0

			if puntuacion_minijuegos == 10 or tiempo_minijuego <= 0: 
				tiempo_minijuego = 0
				if puntuacion_minijuegos == 10: resultado_minijuego = True
				elif tiempo_minijuego <= 0: resultado_minijuego = False
				estado = "FinalMinijuego"
			
			tiempo_inicio = time.get_ticks() - inicio_temporizador
			if tiempo_inicio <= 500:
				T3_TEXT = get_font(75).render("3", True, (255, 255, 255))
				T3_RECT = T3_TEXT.get_rect(center=(640, 300))
				screen.blit(T3_TEXT, T3_RECT)
			elif tiempo_inicio <= 1000:
				T2_TEXT = get_font(75).render("2", True, (255, 255, 255))
				T2_RECT = T2_TEXT.get_rect(center=(640, 300))
				screen.blit(T2_TEXT, T2_RECT)
			elif tiempo_inicio <= 1500:
				T1_TEXT = get_font(75).render("1", True, (255, 255, 255))
				T1_RECT = T1_TEXT.get_rect(center=(640, 300))
				screen.blit(T1_TEXT, T1_RECT)
			elif tiempo_inicio <= 2000:
				GO_TEXT = get_font(75).render("GO!", True, (255, 255, 255))
				GO_RECT = GO_TEXT.get_rect(center=(640, 300))
				screen.blit(GO_TEXT, GO_RECT)

			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()
				if evento.type == MOUSEBUTTONDOWN and tiempo_inicio > 1500:
					if HUEVO1_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo1.x = -100
						tiempo_minijuego -= 50
					if HUEVO2_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo2.x = -100
						puntuacion_minijuegos += 1
					if HUEVO3_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo3.y = -100
						tiempo_minijuego -= 50
					if HUEVO4_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo4.y = -100
						tiempo_minijuego -= 50
					if HUEVO5_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo5.x = -100
						tiempo_minijuego -= 50
					if HUEVO6_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo6.x = -100
						tiempo_minijuego -= 50
					if HUEVO7_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo7.y = -100
						tiempo_minijuego -= 50
					if HUEVO8_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo8.y = -100
						puntuacion_minijuegos += 1
					if HUEVO9_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo9.x = -100
						tiempo_minijuego -= 50
					if HUEVO10_BUTTON.checkForInput(HUEVO_MOUSE_POS):
						huevo10.y = -100
						tiempo_minijuego -= 50
		
		if estado == "Minijuego2":
			screen.fill((0, 0, 0)) 

			PAREJAS_TEXT = get_font(37).render("MATCH THE INGREDIENTS " + str(puntuacion_minijuegos) + "/6", True, (244, 137, 246))
			PAREJAS_RECT = PAREJAS_TEXT.get_rect(center=(640, 100))
			screen.blit(PAREJAS_TEXT, PAREJAS_RECT)

			if tiempo_minijuego <= 750: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 255, 255))

			if tiempo_inicio > 1500:
				tiempo_minijuego -= 1

				if tiempo_minijuego > 750 or pareja1 == True:
					screen.blit(pair1, (pareja11.x, pareja11.y))
					screen.blit(pair1, (pareja12.x, pareja12.y))
				else:
					screen.blit(pair7, (pareja11.x, pareja11.y))
					screen.blit(pair7, (pareja12.x, pareja12.y))
				if tiempo_minijuego > 750 or pareja2 == True:
					screen.blit(pair2, (pareja21.x, pareja21.y))
					screen.blit(pair2, (pareja22.x, pareja22.y))
				else:
					screen.blit(pair7, (pareja21.x, pareja21.y))
					screen.blit(pair7, (pareja22.x, pareja22.y))
				if tiempo_minijuego > 750 or pareja3 == True:
					screen.blit(pair3, (pareja31.x, pareja31.y))
					screen.blit(pair3, (pareja32.x, pareja32.y))
				else:
					screen.blit(pair7, (pareja31.x, pareja31.y))
					screen.blit(pair7, (pareja32.x, pareja32.y))
				if tiempo_minijuego > 750 or pareja4 == True:
					screen.blit(pair4, (pareja41.x, pareja41.y))
					screen.blit(pair4, (pareja42.x, pareja42.y))
				else:
					screen.blit(pair7, (pareja41.x, pareja41.y))
					screen.blit(pair7, (pareja42.x, pareja42.y))
				if tiempo_minijuego > 750 or pareja5 == True:
					screen.blit(pair5, (pareja51.x, pareja51.y))
					screen.blit(pair5, (pareja52.x, pareja52.y))
				else:
					screen.blit(pair7, (pareja51.x, pareja51.y))
					screen.blit(pair7, (pareja52.x, pareja52.y))
				if tiempo_minijuego > 750 or pareja6 == True:
					screen.blit(pair6, (pareja61.x, pareja61.y))
					screen.blit(pair6, (pareja62.x, pareja62.y))
				else:
					screen.blit(pair7, (pareja61.x, pareja61.y))
					screen.blit(pair7, (pareja62.x, pareja62.y))

			if puntuacion_minijuegos == 6 or tiempo_minijuego <= 0: 
				tiempo_minijuego = 0
				if puntuacion_minijuegos == 6: resultado_minijuego = True
				elif tiempo_minijuego <= 0: resultado_minijuego = False
				estado = "FinalMinijuego"
			
			tiempo_inicio = time.get_ticks() - inicio_temporizador
			if tiempo_inicio <= 500:
				T3_TEXT = get_font(75).render("3", True, (255, 255, 255))
				T3_RECT = T3_TEXT.get_rect(center=(640, 300))
				screen.blit(T3_TEXT, T3_RECT)
			elif tiempo_inicio <= 1000:
				T2_TEXT = get_font(75).render("2", True, (255, 255, 255))
				T2_RECT = T2_TEXT.get_rect(center=(640, 300))
				screen.blit(T2_TEXT, T2_RECT)
			elif tiempo_inicio <= 1500:
				T1_TEXT = get_font(75).render("1", True, (255, 255, 255))
				T1_RECT = T1_TEXT.get_rect(center=(640, 300))
				screen.blit(T1_TEXT, T1_RECT)
			elif tiempo_inicio <= 2000:
				GO_TEXT = get_font(75).render("GO!", True, (255, 255, 255))
				GO_RECT = GO_TEXT.get_rect(center=(640, 300))
				screen.blit(GO_TEXT, GO_RECT)

			PAREJAS_MOUSE_POS = mouse.get_pos()
			PAREJA11_BUTTON = Button(image=None, pos=(pareja11.x+75, pareja11.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA12_BUTTON = Button(image=None, pos=(pareja12.x+75, pareja12.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA21_BUTTON = Button(image=None, pos=(pareja21.x+75, pareja21.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA22_BUTTON = Button(image=None, pos=(pareja22.x+75, pareja22.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA31_BUTTON = Button(image=None, pos=(pareja31.x+75, pareja31.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA32_BUTTON = Button(image=None, pos=(pareja32.x+75, pareja32.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA41_BUTTON = Button(image=None, pos=(pareja41.x+75, pareja41.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA42_BUTTON = Button(image=None, pos=(pareja42.x+75, pareja42.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA51_BUTTON = Button(image=None, pos=(pareja51.x+75, pareja51.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA52_BUTTON = Button(image=None, pos=(pareja52.x+75, pareja52.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA61_BUTTON = Button(image=None, pos=(pareja61.x+75, pareja61.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			PAREJA62_BUTTON = Button(image=None, pos=(pareja62.x+75, pareja62.y+100), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()
				if evento.type == MOUSEBUTTONDOWN and tiempo_inicio > 1500:
					if (PAREJA11_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA12_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja1 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 1
						elif pareja == 1: 
							pareja1 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
					if (PAREJA21_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA22_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja2 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 2
						elif pareja == 2: 
							pareja2 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
					if (PAREJA31_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA32_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja3 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 3
						elif pareja == 3: 
							pareja3 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
					if (PAREJA41_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA42_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja4 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 4
						elif pareja == 4: 
							pareja4 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
					if (PAREJA51_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA52_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja5 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 5
						elif pareja == 5: 
							pareja5 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
					if (PAREJA61_BUTTON.checkForInput(PAREJAS_MOUSE_POS) or PAREJA62_BUTTON.checkForInput(PAREJAS_MOUSE_POS)) and pareja6 == False and tiempo_minijuego <= 750:
						if pareja == 0: pareja = 6
						elif pareja == 6: 
							pareja6 = True 
							puntuacion_minijuegos += 1
							pareja = 0
						else: 
							tiempo_minijuego -= 50
							pareja = 0
		
		if estado == "Minijuego3":
			screen.fill((0, 0, 0)) 

			tiempo_minijuego = time.get_ticks() - inicio_temporizador
			segundos = tiempo_minijuego // 1000
			milisegundos = tiempo_minijuego % 1000

			TEMPORIZADOR_TEXT = get_font(37).render("BAKE THE CAKE. REACH 10 SECONDS", True, (244, 137, 246))
			TEMPORIZADOR_RECT = TEMPORIZADOR_TEXT.get_rect(center=(640, 100))
			screen.blit(TEMPORIZADOR_TEXT, TEMPORIZADOR_RECT)

			if tiempo_minijuego <= 3000 and pulsado == False:
				TIEMPO_TEXT = get_font(37).render(f"0{segundos}:{milisegundos:03d}", True, (180, 32, 42))
				TIEMPO_RECT = TIEMPO_TEXT.get_rect(center=(640, 300))
				screen.blit(TIEMPO_TEXT, TIEMPO_RECT)
			elif pulsado == True:
				TIEMPO_TEXT = get_font(37).render(f"0{segundos_final}:{milisegundos_final:03d}", True, (180, 32, 42))
				TIEMPO_RECT = TIEMPO_TEXT.get_rect(center=(640, 300))
				screen.blit(TIEMPO_TEXT, TIEMPO_RECT)

			BOTON_MOUSE_POS = mouse.get_pos()
			BOTON_BUTTON = Button(image=None, pos=(640, 550), text_input="P", font=get_font(150), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(boton, (562.5, 475))

			if pulsado == True: 
				tiempo_minijuego = 0
				if segundos_final == 10: resultado_minijuego = True
				else: resultado_minijuego = False
				estado = "FinalMinijuego"

			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()
				if evento.type == MOUSEBUTTONDOWN:
					if BOTON_BUTTON.checkForInput(BOTON_MOUSE_POS):
						pulsado = True
						segundos_final = tiempo_minijuego // 1000
						milisegundos_final = tiempo_minijuego % 1000
		
		if estado == "Minijuego4":
			screen.fill((0, 0, 0)) 

			BILL_TEXT = get_font(37).render("PAY THE BILL. INPUT FINAL PRICE", True, (244, 137, 246))
			BILL_RECT = BILL_TEXT.get_rect(center=(640, 100))
			screen.blit(BILL_TEXT, BILL_RECT)

			if tiempo_minijuego >= 150: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 255, 255))
			else: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 0, 0))

			if tiempo_minijuego <= 0 or enter == True: 
				tiempo_minijuego = 0
				PF_TEXT2 = get_font(20).render(str(precio_final), True, (255, 255, 255))
				PF_RECT2 = PF_TEXT2.get_rect(center=(960, 640))
				screen.blit(PF_TEXT2, PF_RECT2)
				if precio_bill == precio_final: resultado_minijuego = True
				else: resultado_minijuego = False
				estado = "FinalMinijuego"
			
			tiempo_inicio = time.get_ticks() - inicio_temporizador
			if tiempo_inicio <= 500:
				T3_TEXT = get_font(75).render("3", True, (255, 255, 255))
				T3_RECT = T3_TEXT.get_rect(center=(640, 300))
				screen.blit(T3_TEXT, T3_RECT)
			elif tiempo_inicio <= 1000:
				T2_TEXT = get_font(75).render("2", True, (255, 255, 255))
				T2_RECT = T2_TEXT.get_rect(center=(640, 300))
				screen.blit(T2_TEXT, T2_RECT)
			elif tiempo_inicio <= 1500:
				T1_TEXT = get_font(75).render("1", True, (255, 255, 255))
				T1_RECT = T1_TEXT.get_rect(center=(640, 300))
				screen.blit(T1_TEXT, T1_RECT)
			elif tiempo_inicio <= 2000:
				GO_TEXT = get_font(75).render("GO!", True, (255, 255, 255))
				GO_RECT = GO_TEXT.get_rect(center=(640, 300))
				screen.blit(GO_TEXT, GO_RECT)

			if tiempo_inicio > 1500:
				tiempo_minijuego -= 1
				PRICE_TEXT = get_font(20).render("PRICES", True, (255, 255, 255))
				PRICE_RECT = PRICE_TEXT.get_rect(center=(320, 200))
				screen.blit(PRICE_TEXT, PRICE_RECT)
				EGG_TEXT = get_font(20).render("EGGS............0,5€/unit", True, (255, 255, 255))
				EGG_RECT = EGG_TEXT.get_rect(center=(320, 250))
				screen.blit(EGG_TEXT, EGG_RECT)
				MILK_TEXT = get_font(20).render("MILK..............2€/unit", True, (255, 255, 255))
				MILK_RECT = MILK_TEXT.get_rect(center=(320, 300))
				screen.blit(MILK_TEXT, MILK_RECT)
				CHOCOLATE_TEXT = get_font(20).render("CHOCOLATE.........3€/unit", True, (255, 255, 255))
				CHOCOLATE_RECT = CHOCOLATE_TEXT.get_rect(center=(320, 350))
				screen.blit(CHOCOLATE_TEXT, CHOCOLATE_RECT)
				STRAWBERRY_TEXT = get_font(20).render("STRAWBERRIES....0,2€/unit", True, (255, 255, 255))
				STRAWBERRY_RECT = STRAWBERRY_TEXT.get_rect(center=(320, 400))
				screen.blit(STRAWBERRY_TEXT, STRAWBERRY_RECT)
				CHEESE_TEXT = get_font(20).render("CHEESE............5€/unit", True, (255, 255, 255))
				CHEESE_RECT = CHEESE_TEXT.get_rect(center=(320, 450))
				screen.blit(CHEESE_TEXT, CHEESE_RECT)
				COOKIE_TEXT = get_font(20).render("COOKIES...........1€/unit", True, (255, 255, 255))
				COOKIE_RECT = COOKIE_TEXT.get_rect(center=(320, 500))
				screen.blit(COOKIE_TEXT, COOKIE_RECT)

				BILL_TEXT2 = get_font(20).render("BILL", True, (255, 255, 255))
				BILL_RECT2 = BILL_TEXT2.get_rect(center=(960, 200))
				screen.blit(BILL_TEXT2, BILL_RECT2)
				EGG_TEXT2 = get_font(20).render("EGGS............" + str(eggs_bill) + " units", True, (255, 255, 255))
				EGG_RECT2 = EGG_TEXT2.get_rect(center=(960, 250))
				screen.blit(EGG_TEXT2, EGG_RECT2)
				MILK_TEXT2 = get_font(20).render("MILK............." + str(milk_bill) + " units", True, (255, 255, 255))
				MILK_RECT2 = MILK_TEXT2.get_rect(center=(960, 300))
				screen.blit(MILK_TEXT2, MILK_RECT2)
				CHOCOLATE_TEXT2 = get_font(20).render("CHOCOLATE........" + str(chocolate_bill) + " units", True, (255, 255, 255))
				CHOCOLATE_RECT2 = CHOCOLATE_TEXT2.get_rect(center=(960, 350))
				screen.blit(CHOCOLATE_TEXT2, CHOCOLATE_RECT2)
				STRAWBERRY_TEXT2 = get_font(20).render("STRAWBERRIES...." + str(strawberry_bill) + " units", True, (255, 255, 255))
				STRAWBERRY_RECT2 = STRAWBERRY_TEXT2.get_rect(center=(960, 400))
				screen.blit(STRAWBERRY_TEXT2, STRAWBERRY_RECT2)
				CHEESE_TEXT2 = get_font(20).render("CHEESE..........." + str(cheese_bill) + " units", True, (255, 255, 255))
				CHEESE_RECT2 = CHEESE_TEXT2.get_rect(center=(960, 450))
				screen.blit(CHEESE_TEXT2, CHEESE_RECT2)
				COOKIE_TEXT2 = get_font(20).render("COOKIES.........." + str(cookie_bill) + " units", True, (255, 255, 255))
				COOKIE_RECT2 = COOKIE_TEXT2.get_rect(center=(960, 500))
				screen.blit(COOKIE_TEXT2, COOKIE_RECT2)

			B_MOUSE_POS = mouse.get_pos()
			B1_BUTTON = Button(image=None, pos=(580, 560), text_input="1", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b1, (562.5, 543))
			B2_BUTTON = Button(image=None, pos=(640, 560), text_input="2", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b2, (622.5, 543))
			B3_BUTTON = Button(image=None, pos=(700, 560), text_input="3", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b3, (682.5, 543))
			B4_BUTTON = Button(image=None, pos=(580, 600), text_input="4", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b4, (562.5, 583))
			B5_BUTTON = Button(image=None, pos=(640, 600), text_input="5", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b5, (622.5, 583))
			B6_BUTTON = Button(image=None, pos=(700, 600), text_input="6", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b6, (682.5, 583))
			B7_BUTTON = Button(image=None, pos=(580, 640), text_input="7", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b7, (562.5, 623))
			B8_BUTTON = Button(image=None, pos=(640, 640), text_input="8", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b8, (622.5, 623))
			B9_BUTTON = Button(image=None, pos=(700, 640), text_input="9", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b9, (682.5, 623))
			BBORRAR_BUTTON = Button(image=None, pos=(580, 680), text_input="B", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(bb, (562.5, 663))
			B0_BUTTON = Button(image=None, pos=(640, 680), text_input="0", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(b0, (622.5, 663))
			BENTER_BUTTON = Button(image=None, pos=(700, 680), text_input="E", font=get_font(30), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
			screen.blit(be, (682.5, 663))

			PB_TEXT2 = get_font(20).render(str(precio_bill), True, (255, 255, 255))
			PB_RECT2 = PB_TEXT2.get_rect(center=(960, 600))
			screen.blit(PB_TEXT2, PB_RECT2)

			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()
				if evento.type == MOUSEBUTTONDOWN and tiempo_inicio > 1500:
					if B1_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 1
					if B2_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 2
					if B3_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 3
					if B4_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 4
					if B5_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 5
					if B6_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 6
					if B7_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 7
					if B8_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 8
					if B9_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 9
					if B0_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = (precio_bill * 10) + 0
					if BBORRAR_BUTTON.checkForInput(B_MOUSE_POS):
						precio_bill = precio_bill // 10
					if BENTER_BUTTON.checkForInput(B_MOUSE_POS):
						enter = True
		
		if estado == "Final":
			mixer.music.stop()
			if pisos_tarta == 1:
				if final_sound == False:
					lose_sound.play()
					final_sound = True
				PT1_TEXT = get_font(27).render("WELL... AT LEAST WE HAVE A CAKE", True, (0, 0, 0))
				PT1_RECT = PT1_TEXT.get_rect(center=(640, 300))
				screen.blit(PT1_TEXT, PT1_RECT)
			if pisos_tarta == 2:
				if final_sound == False:
					win2_sound.play()
					final_sound = True
				PT1_TEXT = get_font(27).render("IT'S A SMALL CAKE, BUT IT'S FINE", True, (0, 0, 0))
				PT1_RECT = PT1_TEXT.get_rect(center=(640, 300))
				screen.blit(PT1_TEXT, PT1_RECT)
			if pisos_tarta == 3:
				if final_sound == False:
					win2_sound.play()
					final_sound = True
				PT1_TEXT = get_font(27).render("THAT'S A PRETTY GOOD CAKE!", True, (0, 0, 0))
				PT1_RECT = PT1_TEXT.get_rect(center=(640, 300))
				screen.blit(PT1_TEXT, PT1_RECT)
			if pisos_tarta == 4:
				if final_sound == False:
					win2_sound.play()
					final_sound = True
				PT1_TEXT = get_font(27).render("ALMOST THERE! ONE MORE FLOOR", True, (0, 0, 0))
				PT1_RECT = PT1_TEXT.get_rect(center=(640, 300))
				screen.blit(PT1_TEXT, PT1_RECT)
				PT1_TEXT = get_font(27).render("AND IT WILL BE COMPLETED", True, (0, 0, 0))
				PT1_RECT = PT1_TEXT.get_rect(center=(640, 350))
				screen.blit(PT1_TEXT, PT1_RECT)
			if pisos_tarta == 5:
				if final_sound == False:
					win_sound.play()
					final_sound = True
				PT5_TEXT = get_font(27).render("YOU DID IT! THE CAKE IS COMPLETED", True, (0, 0, 0))
				PT5_RECT = PT5_TEXT.get_rect(center=(640, 300))
				screen.blit(PT5_TEXT, PT5_RECT)
				PT5_TEXT = get_font(27).render("THERE'S ENOUGH CAKE FOR EVERYONE", True, (0, 0, 0))
				PT5_RECT = PT5_TEXT.get_rect(center=(640, 350))
				screen.blit(PT5_TEXT, PT5_RECT)
				PT5_TEXT = get_font(27).render("HAPPY 10TH ANNIVERSARY CRAFTPIX!", True, (0, 0, 0))
				PT5_RECT = PT5_TEXT.get_rect(center=(640, 400))
				screen.blit(PT5_TEXT, PT5_RECT)
			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()

		if estado == "FinalMinijuego":
			tiempo_minijuego -= 1
			if resultado_minijuego == True:
				if tiempo_minijuego == -1: win2_sound.play()
				WIN_TEXT = get_font(37).render("GOOD JOB!", True, (237, 214, 120))
				WIN_RECT = WIN_TEXT.get_rect(center=(640, 400))
				screen.blit(WIN_TEXT, WIN_RECT)
				if tiempo_minijuego <= -200: 
					pisos_tarta += 1
					estado = "Play"
			
			elif resultado_minijuego == False:
				if tiempo_minijuego == -1: lose2_sound.play()
				LOSE_TEXT = get_font(37).render("NICE TRY!", True, (216, 44, 44))
				LOSE_RECT = LOSE_TEXT.get_rect(center=(640, 400))
				screen.blit(LOSE_TEXT, LOSE_RECT)
				if tiempo_minijuego <= -200: 
					estado = "Play"
			
			display.update()
			for evento in event.get():
				if evento.type == QUIT:
					quit()
					exit()
				if evento.type==KEYDOWN:
					if evento.key == K_1 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() - 0.1)
					if evento.key == K_2 and mixer.music.get_volume() > 0.0:
						mixer.music.set_volume(mixer.music.get_volume() + 0.1)
					if evento.key == K_ESCAPE:
						quit()
						exit()

		clock.tick(60)
		await asyncio.sleep(0)

asyncio.run(main())
