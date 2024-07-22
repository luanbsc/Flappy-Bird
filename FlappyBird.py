import pygame
import os

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
birdImage = pygame.image.load(os.path.join('Images', 'birdSprite.png')).convert_alpha()
birdImage = pygame.transform.scale(birdImage, (150, 150))

class Bird(pygame.sprite.Sprite):

    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = birdImage
       self.rect = self.image.get_rect()
       self.rect.center = (screen.get_width()/2, screen.get_height()/2)
       self.velocidade_queda = 0
       self.move_up = False

    def update(self):
        if self.velocidade_queda < 10:
            self.velocidade_queda += 0.5
        if self.move_up:
            self.velocidade_queda = -10
            self.rect.y -= 700 * dt
            self.move_up = False
        self.rect.y += self.velocidade_queda

spritePlayer = pygame.sprite.Group()
bird = Bird()
spritePlayer.add(bird)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bird.move_up = True

    # Limitar FPS em 60
    dt = clock.tick(60) / 1000

    # Chamar o update() do Bird
    spritePlayer.update()

    # BackGround do jogo
    screen.fill("purple")

    # Desenhar o Bird na tela
    spritePlayer.draw(screen)

    # Atualizar tela
    pygame.display.flip()


pygame.quit()