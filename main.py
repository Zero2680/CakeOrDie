from pygame import *
init()
from random import *
from button import Button
from math import *
import asyncio
screen = display.set_mode((1280, 720), FULLSCREEN)
display.set_caption('Fire Game')
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

async def main():
    global salto, angulo, x_jump, salto_doble, w, correr, suelo, x_sup, jump, quieto
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
    estado = "Menu"
    plataforma = Bola(300,350,15,30, 1, 1, 0, (0,0,255), 100, 0)
    enemigo = Bola(615,50,50,50, 1, 1, 0, (255,0,0), 100, 0)
    suelo1 = Bola(0, 599, 1280, 300, 1, 1, 0, (0, 0, 0), 0, 0)
    animacion_run = 0
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
            screen.blit(cake, (enemigo.x-75, enemigo.y))

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
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())