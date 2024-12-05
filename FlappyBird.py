import pygame
import os
import random
import math

# Salvando caminho do diretorio em que se encontra a pasta do jogo
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Definindo o diretorio de trabalho como o diretorio em que se encontra o jogo
os.chdir(script_dir)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((360, 640))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
running = True
dt = 0

# Carregando imagens
birdImage = pygame.image.load(os.path.join('Images', 'birdSprite.png'))
birdImage = pygame.transform.scale(birdImage, (100, 100))
background = pygame.image.load(os.path.join('Images', 'background.png'))
background = pygame.transform.scale(background, (background.get_rect().w, 640))
background_ground = pygame.image.load(os.path.join('Images', 'ground.png'))
background_ground = pygame.transform.scale(background_ground, (background_ground.get_rect().w, 80))
pipe_lowerImage = pygame.image.load(os.path.join('Images', 'pipe.png'))
pipe_lowerImage = pipe_topImage = pygame.transform.scale(pipe_lowerImage, (90, 178))
pipe_topImage = pygame.image.load(os.path.join('Images', 'pipe.png'))
pipe_topImage = pygame.transform.flip(pipe_topImage, False, True)
pipe_topImage = pygame.transform.scale(pipe_topImage, (90, 178))
pipe_body = pygame.image.load(os.path.join('Images', 'pipe_body.png'))
pipe_end = pygame.image.load(os.path.join('Images', 'pipe_end.png'))

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdImage
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, screen.get_height()/2)
        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, 48, 36)
        self.velocidade_queda = 0
        self.move_up = False
        self.game_over = False

    def update(self):
        self.rect.y += self.velocidade_queda
        if self.velocidade_queda < 10:
            self.velocidade_queda += 0.5
        if self.move_up:
            self.velocidade_queda = -8
            self.move_up = False
        if self.rect.y < -120:
            self.rect.y = -120
        if self.hitbox.bottom >= 580:
            self.rect.y = 515
            self.game_over = True
        self.hitbox.center = (self.rect.x + 50, self.rect.y + 52)

class pipeBody(pygame.sprite.Sprite):
    def __init__(self, tamanho, lower=0, nmr_pipe=0):
        pygame.sprite.Sprite.__init__(self)
        self.tamanho = tamanho
        self.image = pipe_body
        self.image = pygame.transform.scale(self.image, (80, self.tamanho))
        self.rect = self.image.get_rect()
        self.rect.left = screen.get_width()
        if nmr_pipe == 1:
            self.rect.left += 270
        elif nmr_pipe == 2:
            self.rect.left += 100
        if lower == 1:
            self.rect.bottom = 580
        else:
            self.rect.top = 0
        self.hitbox = pygame.Rect(self.rect.left + 4, self.rect.top, self.rect.w - 8, self.rect.h)

class pipeEnd(pygame.sprite.Sprite):
    def __init__(self, tamanho, lower=0, nmr_pipe=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_end
        self.rect = self.image.get_rect()
        self.rect.left = screen.get_width()
        if nmr_pipe == 1:
            self.rect.left += 270
        elif nmr_pipe == 2:
            self.rect.left += 100
        if lower == 1:
            self.rect.top = 580 - tamanho - 32
        else:
            self.rect.top = tamanho
        self.hitbox = pygame.Rect(self.rect.top, self.rect.left, self.rect.w, self.rect.h)

class LowerPipe(pygame.sprite.Sprite):
    def __init__(self, nmr_pipe=0):
       pygame.sprite.Sprite.__init__(self)
       self.tamanho = random.randint(32, 390)
       print(self.tamanho)
       self.pipe_body = pipeBody(self.tamanho, 1, nmr_pipe)
       self.pipe_end = pipeEnd(self.tamanho, 1, nmr_pipe)

    def update(self):
        self.pipe_body.rect.x -= 2
        self.pipe_body.hitbox.top = self.pipe_body.rect.top
        self.pipe_body.hitbox.left = self.pipe_body.rect.left + 4
        self.pipe_end.rect.x -= 2
        self.pipe_end.hitbox.top = self.pipe_end.rect.top
        self.pipe_end.hitbox.left = self.pipe_end.rect.left

class TopPipe(pygame.sprite.Sprite):
    def __init__(self, tamanho, nmr_pipe=0):
       pygame.sprite.Sprite.__init__(self)
       self.tamanho = 580 - tamanho - 32 - 126 - 32
       print(self.tamanho)
       self.pipe_body = pipeBody(self.tamanho, ..., nmr_pipe)
       self.pipe_end = pipeEnd(self.tamanho, ..., nmr_pipe)

    def update(self):
        self.pipe_body.rect.x -= 2
        self.pipe_body.hitbox.top = self.pipe_body.rect.top
        self.pipe_body.hitbox.left = self.pipe_body.rect.left + 4
        self.pipe_end.rect.x -= 2
        self.pipe_end.hitbox.top = self.pipe_end.rect.top
        self.pipe_end.hitbox.left = self.pipe_end.rect.left

# Instanciando objetos e variaveis de controle
# Bird
spritePlayer = pygame.sprite.Group()
bird = Bird()
spritePlayer.add(bird)
bg_x1 = 0

# Pipes
pipes = pygame.sprite.Group() # Grupo dos pipes

# Primeiro LowerPipe
lp1 = LowerPipe()
pipes.add(lp1.pipe_body)
pipes.add(lp1.pipe_end)

# Primeiro TopPipe
tp1 = TopPipe(lp1.tamanho)
pipes.add(tp1.pipe_body)
pipes.add(tp1.pipe_end)

# Segundo LowerPipe
lp2 = LowerPipe(1)
pipes.add(lp2.pipe_body)
pipes.add(lp2.pipe_end)

# Segundo TopPipe
tp2 = TopPipe(lp2.tamanho, 1)
pipes.add(tp2.pipe_body)
pipes.add(tp2.pipe_end)

rects_pipes = []
for sprite in pipes.sprites():
    rects_pipes.append(sprite.hitbox)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bird.move_up = True

    #print(bird.rect.y)

    # Limitar FPS em 60
    dt = clock.tick(60) / 1000

    # Chamar o update() caso o jogo não esteja em estado de game over
    if not bird.game_over:
        spritePlayer.update()
        pipes.update()
        tp1.update()
        lp1.update()
        tp2.update()
        lp2.update()
        bg_x1 -= 2

    # Mudar o posicionamento do primeiro pipe após passar da tela
    if lp1.pipe_body.rect.right <= 0:
        lp1.kill()
        tp1.kill()
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        lp1 = LowerPipe(2)
        pipes.add(lp1.pipe_body)
        pipes.add(lp1.pipe_end)
        tp1 = TopPipe(lp1.tamanho, 2)
        pipes.add(tp1.pipe_body)
        pipes.add(tp1.pipe_end)
        rects_pipes.append(lp1.pipe_body)
        rects_pipes.append(lp1.pipe_end)
        rects_pipes.append(tp1.pipe_body)
        rects_pipes.append(tp1.pipe_end)

    # Mudar o posicionamento do segundo pipe após passar da tela
    if lp2.pipe_body.rect.right <= 0:
        lp2.kill()
        tp2.kill()
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        rects_pipes.pop(0)
        lp2 = LowerPipe(2)
        pipes.add(lp2.pipe_body)
        pipes.add(lp2.pipe_end)
        tp2 = TopPipe(lp2.tamanho, 2)
        pipes.add(tp2.pipe_body)
        pipes.add(tp2.pipe_end)
        rects_pipes.append(lp2.pipe_body)
        rects_pipes.append(lp2.pipe_end)
        rects_pipes.append(tp2.pipe_body)
        rects_pipes.append(tp2.pipe_end)

    # Colisão
    if pygame.Rect.collidelist(bird.hitbox, rects_pipes) != -1:
        bird.game_over = True

    # Reseta a posição do fundo para a imagem ficar em looping
    if bg_x1 <= -300:
        bg_x1 = 0

    # Desenhar o BackGround do jogo
    screen.blit(background, (bg_x1, 0))
    screen.blit(background_ground, (bg_x1, 580))

    # Desenhar o Bird na tela
    spritePlayer.draw(screen)

    # Desenhar os canos na tela
    pipes.draw(screen)

    # Desenhos das hitbox para teste
    #pygame.draw.rect(screen, (100, 0, 0), bird.hitbox, 2)

    #pygame.draw.rect(screen, (0, 0, 255), lp1.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), lp1.pipe_end.hitbox, 2)
    #pygame.draw.rect(screen, (0, 0, 255), tp1.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), tp1.pipe_end.hitbox, 2)

    #pygame.draw.rect(screen, (0, 0, 255), lp2.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), lp2.pipe_end.hitbox, 2)
    #pygame.draw.rect(screen, (0, 0, 255), tp2.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), tp2.pipe_end.hitbox, 2)

    # Atualizar tela
    pygame.display.flip()


pygame.quit()