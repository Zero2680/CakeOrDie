from pygame import *
init()
from random import *
from button import Button
from math import *
import asyncio
screen = display.set_mode((1280, 720), FULLSCREEN)
display.set_caption('Cake or Die')
screen.fill((0, 0, 0)) 

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
			self.direcciony = 1
		if self.y >= 599:
			self.direcciony = 0
    
	def MovimientoGelatina(self, plataforma):
		if self.check_colisiones(plataforma) == True:
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
			self.direcciony = 0
    
	def MovimientoTortitas(self, plataforma):
		if self.check_colisiones(plataforma) == True:
			plataforma.vidas -= 1
			self.x = 1280
		if self.direccionx == 0:
			self.x -= 5
		if self.direccionx == 1:
			self.x += 5
		if self.x <= 0 and self.direccionx == 0:
			self.x = 1260
		if self.x >= 1280 and self.direccionx == 1:
			self.x = 0
    
	def MovimientoDonut(self, plataforma):
		if self.check_colisiones(plataforma):
			plataforma.vidas -= 1
			self.y = -100
		if self.y < 600:
			if self.y == -100:
				self.x = randrange(1, 13) * 100
			self.y += 4
		if self.y >= 600:
			self.y = -100

	def MovimientoHuevo(self, plataforma):
		global puntuacion_minijuegos
		if self.check_colisiones(plataforma):
			plataforma.vidas -= 1
			self.y = -100
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

async def main():
	global salto, angulo, x_jump, salto_doble, w, correr, suelo, x_sup, jump, quieto, puntuacion_minijuegos, pisos_tarta
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
	plataforma = Bola(300,350,15,30, 1, 1, 0, (0,0,255), 100, 0)
	enemigo = Bola(615,50,50,50, 1, 1, 0, (255,0,0), 100, 0)
	suelo1 = Bola(0, 599, 1280, 300, 1, 1, 0, (0, 0, 0), 0, 0)
	limon1 = Bola(0,0,15,15, 1, 1, 0, (0,255,0), 100, 0)
	gelatina1 = Bola(0,100,15,15, 1, 1, 0, (0,255,0), 100, 0)
	tortita1 = Bola(0,550,30,50, 1, 1, 0, (0,255,0), 100, 0)
	donut1 = Bola(0,0,15,15, 1, 1, 0, (0,255,0), 100, 0)
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
	animacion_run = 0
	animacion_huevo = 0
	tiempo_minijuego = 750
	while True:
		if estado == "Menu":
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
			OPTIONS_MOUSE_POS = mouse.get_pos()

			#screen.blit(BG, (0, 0))
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
			plataforma.DibujarObjeto()

			enemigo.DibujarObjeto()
			if pisos_tarta == 1: screen.blit(cake1, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 2: screen.blit(cake2, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 3: screen.blit(cake3, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 4: screen.blit(cake4, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 5: screen.blit(cake5, (enemigo.x-75, enemigo.y))
			elif pisos_tarta == 6: screen.blit(cake, (enemigo.x-75, enemigo.y))

			#ANIMACIÓN LEMON
			#limon1.MovimientoLemon(plataforma)
			#limon1.DibujarObjeto()
			#if limon1.direccionx == 1:
			#    screen.blit(lemon, (limon1.x-10, limon1.y-10))
			#else:
			#    screen.blit(lemon, (limon1.x-10, limon1.y-10))

			#ANIMACIÓN GELATINA
			#gelatina1.MovimientoGelatina(plataforma)
			#gelatina1.DibujarObjeto()
			#screen.blit(jelly, (gelatina1.x-10, gelatina1.y-10))
			
			#ANIMACIÓN TORTITA
			#tortita1.MovimientoTortitas(plataforma)
			#tortita1.DibujarObjeto()
			#screen.blit(pancake, (tortita1.x-20, tortita1.y-5))

			#ANIMACIÓN DONUT
			#donut1.MovimientoDonut(plataforma)
			#donut1.DibujarObjeto()
			#screen.blit(dona, (donut1.x-17.5, donut1.y-22.5))

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
					if evento.key == K_k:
						estado = "Minijuego1"

		if estado == "Minijuego1":
			if tiempo_minijuego >= 0 and puntuacion_minijuegos < 10:
				screen.fill((0, 0, 0)) 
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

				if tiempo_minijuego >= 150: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 255, 255))
				else: barra_tiempo(screen, 340, 150, tiempo_minijuego/2.5, (255, 0, 0))

				tiempo_minijuego -= 1
				animacion_huevo += 1

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
		
		if estado == "FinalMinijuego":
			tiempo_minijuego -= 1
			if puntuacion_minijuegos == 10:
				WIN_TEXT = get_font(37).render("GOOD JOB!", True, (237, 214, 120))
				WIN_RECT = WIN_TEXT.get_rect(center=(640, 400))
				screen.blit(WIN_TEXT, WIN_RECT)
				if tiempo_minijuego <= -200: 
					pisos_tarta += 1
					estado = "Play"
			
			elif tiempo_minijuego < 0:
				LOSE_TEXT = get_font(37).render("NICE TRY!", True, (216, 44, 44))
				LOSE_RECT = LOSE_TEXT.get_rect(center=(640, 400))
				screen.blit(LOSE_TEXT, LOSE_RECT)
				if tiempo_minijuego <= -200: estado = "Play"
			
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
