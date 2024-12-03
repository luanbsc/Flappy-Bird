import pygame
import os
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
pipe_lowerImage = pygame.image.load(os.path.join('Images', 'pipe.png'))
pipe_lowerImage = pipe_topImage = pygame.transform.scale(pipe_lowerImage, (90, 178))
pipe_topImage = pygame.image.load(os.path.join('Images', 'pipe.png'))
pipe_topImage = pygame.transform.flip(pipe_topImage, False, True)
pipe_topImage = pygame.transform.scale(pipe_topImage, (90, 178))

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdImage
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, screen.get_height()/2)
        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, 40, 40)
        self.velocidade_queda = 0
        self.move_up = False
        self.game_over = False

    def update(self):
        self.hitbox.center = (self.rect.x + 50, self.rect.y + 56)
        self.rect.y += self.velocidade_queda
        if self.velocidade_queda < 10:
            self.velocidade_queda += 0.5
        if self.move_up:
            self.velocidade_queda = -10
            self.rect.y -= 700 * dt
            self.move_up = False
        if self.rect.y < -120:
            self.rect.y = -120
        if self.rect.y >= 535:
            self.rect.y = 535
            self.game_over = True

    def check_collision(self, pipes):
        for pipe in pipes:
            if math.dist(self.rect.center, pipe.rect.center) <= self.radius + (pipe.rect.width / 2):
                return True
        return False

class LowerPipe(pygame.sprite.Sprite):

    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pipe_lowerImage
       self.rect = self.image.get_rect()
       self.rect.center = (screen.get_width()/2, screen.get_height()/2)

    def update(self):
        pass

class TopPipe(pygame.sprite.Sprite):

    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pipe_topImage
       self.rect = self.image.get_rect()
       self.rect.center = (screen.get_width(), screen.get_height()/2)

    def update(self):
        self.rect.x -= 2

# Instanciando objetos e variaveis de controle
# Bird
spritePlayer = pygame.sprite.Group()
bird = Bird()
spritePlayer.add(bird)
bg_x1 = 0

# Pipes
pipes = pygame.sprite.Group()
teste = TopPipe()
pipes.add(teste)
rects_pipes = []
for sprite in pipes.sprites():
    rects_pipes.append(sprite.rect)

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

    # Chamar o update() do Bird
    if not bird.game_over:
        spritePlayer.update()
        pipes.update()
        bg_x1 -= 2
    
    # Colisão
    if pygame.Rect.collidelist(bird.hitbox, rects_pipes) != -1:
        bird.game_over = True

    # Reseta a posição do fundo para a imagem ficar em looping
    if bg_x1 <= -300:
        bg_x1 = 0

    # Desenhar o BackGround do jogo
    screen.blit(background, (bg_x1, 0))

    # Desenhar o Bird na tela
    spritePlayer.draw(screen)
    pipes.draw(screen)
    pygame.draw.rect(screen, (100, 0, 0, 0), bird.hitbox, 2)

    # Atualizar tela
    pygame.display.flip()


pygame.quit()