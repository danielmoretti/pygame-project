import pygame
import time
from pygame.locals import *
import random, math, sys
pygame.init()

#Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Tamanho da tela do jogo
Surface = pygame.display.set_mode((800,600))

#Lista de inimigos
Circulos = []


clock = pygame.time.Clock()

#Fontes
title_font = pygame.font.SysFont("Comic Sans Ms", 100)
title_font2 = pygame.font.SysFont("Comic Sans Ms", 20)
FONT = pygame.font.SysFont("Comic Sans Ms", 40)

menu=True
#Titulo de inicio
menu_title = title = title_font.render("CrazyBalls", True, WHITE)
menu_title2 = title = title_font2.render("Pressione o botao esquerdo do mouse para iniciar", True, WHITE)

#Iniciando o Jogo
title_inicio = title = title_font.render("Iniciando...", True, WHITE)



class Circulo:

    def __init__(self):

        self.radius = 30
        self.x = random.randint(self.radius, 800-self.radius)
        self.y = random.randint(self.radius, 600-self.radius)
        self.speedx = 0.5*(random.random()+1.0)
        self.speedy = 0.5*(random.random()+1.0)

# Quantidade de inimigos
for i in range(5):
    Circulos.append(Circulo())



#Calcular colisoes entre os inimigos e nas bordas da tela
def CircleCollide(C1,C2):
    C1Speed = math.sqrt((C1.speedx**2)+(C1.speedy**2))
    XDiff = -(C1.x-C2.x)
    YDiff = -(C1.y-C2.y)
    if XDiff > 0:
        if YDiff > 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff < 0:
        if YDiff > 0:
            Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
        elif YDiff < 0:
            Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
            XSpeed = -C1Speed*math.cos(math.radians(Angle))
            YSpeed = -C1Speed*math.sin(math.radians(Angle))
    elif XDiff == 0:
        if YDiff > 0:
            Angle = -90
        else:
            Angle = 90
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    elif YDiff == 0:
        if XDiff < 0:
            Angle = 0
        else:
            Angle = 180
        XSpeed = C1Speed*math.cos(math.radians(Angle))
        YSpeed = C1Speed*math.sin(math.radians(Angle))
    C1.speedx = XSpeed
    C1.speedy = YSpeed

        

#Detectar colisao bola Azul X Vermelha
def CollisionDetect():
    Surface.fill(BLACK)
    raio = 10
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    pygame.draw.circle(Surface, (0, 0, 255), (x , y), raio)
    mouse = pygame.rect.Rect(x-10, y-10, 20, 20)
    for Circulo in Circulos:
        rect_circulo = pygame.rect.Rect(int(Circulo.x)-30, int(600-Circulo.y)-30, Circulo.radius * 2, Circulo.radius * 2)
        if(rect_circulo.colliderect(mouse)):
            # Start playback
            a = pygame.mixer.Sound("colidiu.wav")
            a.play()
            time.sleep(5)
            pygame.quit(); sys.exit()
        for Circulo2 in Circulos:
            if Circulo != Circulo2:
                if math.sqrt(  ((Circulo.x-Circulo2.x)**2)  +  ((Circulo.y-Circulo2.y)**2)  ) <= (Circulo.radius+Circulo2.radius):
                    #Utilizando a funcao que calcula o rebote
                    CircleCollide(Circulo,Circulo2)
                    s = pygame.mixer.Sound("batevermelha.wav")
                    s.play()

def movimento():
    Surface.fill(BLACK)
    raio = 10
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    pygame.draw.circle(Surface, (0, 0, 255), (x , y), raio)
    for Circulo in Circulos:
        pygame.draw.circle(Surface, RED, (int(Circulo.x), int(600-Circulo.y)), Circulo.radius)
    for Circulo in Circulos:
        Circulo.x += Circulo.speedx
        Circulo.y += Circulo.speedy

        if Circulo.y > 580 or Circulo.y < 0:
            Circulo.speedy = Circulo.speedy * -1
            s = pygame.mixer.Sound("batevermelha.wav")
            s.play()
        if Circulo.x > 780 or Circulo.x < 0:
            Circulo.speedx = Circulo.speedx * -1
            s = pygame.mixer.Sound("batevermelha.wav")
            s.play()

    pygame.display.flip()


def GetInput():
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit(); sys.exit()

def menu():
    menu = True
    while menu:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Surface.blit(title_inicio,(150, 500))
                    menu = False

        pygame.display.update()
        Surface.fill(BLACK)
        Surface.blit(menu_title, (200, 250))
        Surface.blit(menu_title2,(150, 450))
        clock.tick(30)

'''def Time():
    sys.stdout.flush()
    time.sleep(15)
    sys.stdout.flush()'''
    



def main():
        menu()
        sys.stdout.flush()
        time.sleep(3)
        sys.stdout.flush()
        print("Jogo inicia")
        while True:    
            GetInput()
            movimento()
            CollisionDetect()


if __name__ == '__main__': main()
