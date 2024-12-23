import pygame
import os
import random
import json

# Salvando caminho do diretorio em que se encontra a pasta do jogo
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Definindo o diretorio de trabalho como o diretorio em que se encontra o jogo
os.chdir(script_dir)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((440, 640))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
running = True
dt = 0

# Carregando imagens
birdImage = pygame.image.load(os.path.join('Assets\\images', 'Sprite2.png'))
birdImage = pygame.transform.scale(birdImage, (100, 100))
birdImage_f1 = pygame.image.load(os.path.join('Assets\\images', 'Sprite1.png'))
birdImage_f1 = pygame.transform.scale(birdImage_f1, (100, 100))
birdImage_f2 = pygame.image.load(os.path.join('Assets\\images', 'Sprite3.png'))
birdImage_f2 = pygame.transform.scale(birdImage_f2, (100, 100))
background = pygame.image.load(os.path.join('Assets\\images', 'spr_bg.png'))
background = pygame.transform.scale(background, (440, 640))
background_ground = pygame.image.load(os.path.join('Assets\\images', 'ground.png'))
background_ground = pygame.transform.scale(background_ground, (background_ground.get_rect().w, 80))
pipe_body = pygame.image.load(os.path.join('Assets\\images', 'pipe_body.png'))
pipe_end = pygame.image.load(os.path.join('Assets\\images', 'pipe_end.png'))
w_p = pygame.image.load(os.path.join('Assets\\images', 'tile_0358.png'))
w_p = pygame.transform.scale(w_p, (64, 64))
w_b = pygame.image.load(os.path.join('Assets\\images', 'tile_0086.png'))
w_b = pygame.transform.scale(w_b, (64, 64))
painel = pygame.image.load(os.path.join('Assets\\images', 'panel.png'))
painel = pygame.transform.scale(painel, (339, 171))
gameover = pygame.image.load(os.path.join('Assets\\images', 'gameover.png'))
gameover = pygame.transform.scale(gameover, (294, 66))
getready = pygame.image.load(os.path.join('Assets\\images', 'getready.png'))
getready = pygame.transform.scale(getready, (285, 75))
flappybird = pygame.image.load(os.path.join('Assets\\images', 'title.png'))
flappybird = pygame.transform.scale(flappybird, (267, 72))
button_ok = pygame.image.load(os.path.join('Assets\\images', 'ok.png'))
button_ok = pygame.transform.scale(button_ok, (120, 42))
button_start = pygame.image.load(os.path.join('Assets\\images', 'start.png'))
button_start = pygame.transform.scale(button_start, (120, 42))
button_quit = pygame.image.load(os.path.join('Assets\\images', 'quit.png'))
button_quit = pygame.transform.scale(button_quit, (120, 42))
medalha_bronze = pygame.image.load(os.path.join('Assets\\images', 'bronze.png'))
medalha_bronze = pygame.transform.scale(medalha_bronze, (96, 96))
medalha_silver = pygame.image.load(os.path.join('Assets\\images', 'silver.png'))
medalha_silver = pygame.transform.scale(medalha_silver, (96, 96))
medalha_gold = pygame.image.load(os.path.join('Assets\\images', 'gold.png'))
medalha_gold = pygame.transform.scale(medalha_gold, (96, 96))

# Carregando fontes
fonte_numero = pygame.font.Font("Assets\\font\\flappy-font-number.ttf", 30)
fonte_texto = pygame.font.Font("Assets\\font\\flappy-font-text.ttf", 48)
fonte_texto_bg = pygame.font.Font("Assets\\font\\flappy-font-text.ttf", 49)
fonte_menu = pygame.font.Font("Assets\\font\\Minecraft.ttf", 24)
fonte_menu_panel = pygame.font.Font("Assets\\font\\Minecraft.ttf", 20)
fonte_title_bg = pygame.font.Font("Assets\\font\\flappy-font-text.ttf", 50)
fonte_title = pygame.font.Font("Assets\\font\\FlappyBirdy.ttf", 80)
fonte_title_bg2 = pygame.font.Font("Assets\\font\\FlappyBirdy.ttf", 84)

# Carregando áudios
sfx_asas = pygame.mixer.Sound("Assets\\sons\\sfx_wing.wav")
sfx_alterna_aba = pygame.mixer.Sound("Assets\\sons\\sfx_swooshing.wav")
sfx_ponto = pygame.mixer.Sound("Assets\\sons\\sfx_point.wav")
sfx_hit = pygame.mixer.Sound("Assets\\sons\\sfx_hit.wav")
sfx_die = pygame.mixer.Sound("Assets\\sons\\sfx_die.wav")

# Classe do Pássaro
class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = birdImage
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/4, screen.get_height()/2)
        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, 40, 36)
        self.velocidade_queda = 0
        self.move_up = False
        self.game_over = False
        self.angle_rotate = 0
        self.rect_rotated = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.rotate(self.image_original, self.angle_rotate)
        self.rect_rotated = self.image.get_rect(center=(screen.get_width()/4, self.rect.y + 50))
        self.rect.y += self.velocidade_queda
        if self.velocidade_queda < 10:
            self.velocidade_queda += 0.5
        if self.move_up and not self.game_over:
            self.angle_rotate = 50
            self.velocidade_queda = -8
            self.move_up = False
            sfx_asas.play()
        if self.rect.y < -120:
            self.rect.y = -120
        if not self.game_over and self.hitbox.bottom >= 580:
            sfx_hit.play()
            self.rect.y = 515
            self.game_over = True
        self.hitbox.center = (self.rect.x + 50, self.rect.y + 52)
        if self.angle_rotate >= -50:
            self.angle_rotate -= 2
        
        if self.game_over:
            if self.hitbox.bottom < 580:
                self.rect.y += self.velocidade_queda
            else:
                self.rect.y = 515
    
    def reset(self):
        self.rect.center = (screen.get_width()/4, screen.get_height()/2)
        self.hitbox.center = (self.rect.x + 50, self.rect.y + 52)

# Classe do corpo dos pipes
class pipeBody(pygame.sprite.Sprite):
    def __init__(self, tamanho, lower=0, nmr_pipe=0):
        pygame.sprite.Sprite.__init__(self)
        self.tamanho = tamanho
        self.image = pipe_body
        if lower == 1:
            self.image = pygame.transform.scale(self.image, (80, self.tamanho))
        else:
            self.image = pygame.transform.scale(self.image, (80, self.tamanho + 120))
        self.rect = self.image.get_rect()
        self.rect.left = screen.get_width()
        if nmr_pipe == 1:
            self.rect.left += 220
        elif nmr_pipe == 2:
            self.rect.left += 440
        elif nmr_pipe != 0:
            self.rect.left = nmr_pipe
        if lower == 1:
            self.rect.bottom = 580
            self.hitbox = pygame.Rect(self.rect.left + 4, self.rect.top, self.rect.w - 8, self.rect.h)
        else:
            self.rect.top = -120
            self.hitbox = pygame.Rect(self.rect.left + 4, self.rect.top, self.rect.w - 8, self.rect.h)

# Classe da cabeça dos pipes
class pipeEnd(pygame.sprite.Sprite):
    def __init__(self, tamanho, lower=0, nmr_pipe=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_end
        self.rect = self.image.get_rect()
        self.rect.left = screen.get_width()
        if nmr_pipe == 1:
            self.rect.left += 220
        elif nmr_pipe == 2:
            self.rect.left += 440
        elif nmr_pipe != 0:
            self.rect.left = nmr_pipe
        if lower == 1:
            self.rect.top = 580 - tamanho - 32
        else:
            self.rect.top = tamanho
        self.hitbox = pygame.Rect(self.rect.top, self.rect.left, self.rect.w, self.rect.h)

# Classe que constroi o pipe inferior, juntando as classes corpo e cabeça do pipe
class LowerPipe(pygame.sprite.Sprite):
    def __init__(self, nmr_pipe=0):
       pygame.sprite.Sprite.__init__(self)
       self.tamanho = random.randint(32, 390)
       self.pipe_body = pipeBody(self.tamanho, 1, nmr_pipe)
       self.pipe_end = pipeEnd(self.tamanho, 1, nmr_pipe)

    def update(self):
        self.pipe_body.rect.x -= 2
        self.pipe_body.hitbox.top = self.pipe_body.rect.top
        self.pipe_body.hitbox.left = self.pipe_body.rect.left + 4
        self.pipe_end.rect.x -= 2
        self.pipe_end.hitbox.top = self.pipe_end.rect.top
        self.pipe_end.hitbox.left = self.pipe_end.rect.left

# Classe que constroi o pipe superior, juntando as classes corpo e cabeça do pipe
class TopPipe(pygame.sprite.Sprite):
    def __init__(self, tamanho, nmr_pipe=0):
       pygame.sprite.Sprite.__init__(self)
       self.tamanho = 580 - tamanho - 32 - 126 - 32
       self.pipe_body = pipeBody(self.tamanho, ..., nmr_pipe)
       self.pipe_end = pipeEnd(self.tamanho, ..., nmr_pipe)

    def update(self):
        self.pipe_body.rect.x -= 2
        self.pipe_body.hitbox.top = self.pipe_body.rect.top
        self.pipe_body.hitbox.left = self.pipe_body.rect.left + 4
        self.pipe_end.rect.x -= 2
        self.pipe_end.hitbox.top = self.pipe_end.rect.top
        self.pipe_end.hitbox.left = self.pipe_end.rect.left

# ---------------- Instanciando objetos e variaveis de controle ---------------- #
# Bird
spritePlayer = pygame.sprite.Group()
bird = Bird()
spritePlayer.add(bird)

# Pipes
pipes = pygame.sprite.Group() # Grupo dos pipes

# ---------------- Primeiro pipe ----------------#
# Primeiro LowerPipe
lp1 = LowerPipe()
pipes.add(lp1.pipe_body)
pipes.add(lp1.pipe_end)

# Primeiro TopPipe
tp1 = TopPipe(lp1.tamanho)
pipes.add(tp1.pipe_body)
pipes.add(tp1.pipe_end)

# ---------------- Segundo pipe ---------------- #
# Segundo LowerPipe
lp2 = LowerPipe(1)
pipes.add(lp2.pipe_body)
pipes.add(lp2.pipe_end)

# Segundo TopPipe
tp2 = TopPipe(lp2.tamanho, 1)
pipes.add(tp2.pipe_body)
pipes.add(tp2.pipe_end)

# ---------------- Terceiro pipe ---------------- #
# Terceiro LowerPipe
lp3 = LowerPipe(2)
pipes.add(lp3.pipe_body)
pipes.add(lp3.pipe_end)

# Terceiro TopPipe
tp3 = TopPipe(lp3.tamanho, 2)
pipes.add(tp3.pipe_body)
pipes.add(tp3.pipe_end)

# Lista contendo as hitbox dos pipes
rects_pipes = []
for sprite in pipes.sprites():
    rects_pipes.append(sprite.hitbox)

# Criação de evento para alterar imagem da tecla W a cada 0,5 segundos
w_troca = pygame.USEREVENT + 1
pygame.time.set_timer(w_troca, 500)

# Criação de evento para fazer animação do pássaro batendo as asas
birdImage_troca = pygame.USEREVENT + 2
pygame.time.set_timer(birdImage_troca, 100)

# Variável que permite a repetição do jogo
restart = True

# Criando um efeito de transição de tela
fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
fade_surface.fill((0, 0, 0))
# Variáveis para controlar o efeito
fade_in = False
fade_out = False
alpha = 0

# Looping do jogo
while running:
    # Reinicializar as variáveis para recomeçar o jogo a partir do menu
    if restart:
        restart = False

        # Score
        score = "0"
        score_animation = "0"
        highscore_animation = "0"

        # Variáveis de controle
        menu = True
        start = False
        conta_pontos = 0
        bg_x1 = 0
        title_x = 0
        title_sobe = True
        bird.game_over = False
        frame = 0

        highscr = 0
        if os.path.exists("scr.bin"):
            # Carregar HighScore caso exista
            with open("scr.bin", "rb") as arquivo:
                highscr_bin = arquivo.read()
                highscr = json.loads(highscr_bin.decode("utf-8"))

        # Reiniciando o grupo de pipes
        pipes.empty()

        # ---------------- Primeiro pipe ----------------#
        # Primeiro LowerPipe
        lp1 = LowerPipe()
        pipes.add(lp1.pipe_body)
        pipes.add(lp1.pipe_end)

        # Primeiro TopPipe
        tp1 = TopPipe(lp1.tamanho)
        pipes.add(tp1.pipe_body)
        pipes.add(tp1.pipe_end)

        # ---------------- Segundo pipe ---------------- #
        # Segundo LowerPipe
        lp2 = LowerPipe(1)
        pipes.add(lp2.pipe_body)
        pipes.add(lp2.pipe_end)

        # Segundo TopPipe
        tp2 = TopPipe(lp2.tamanho, 1)
        pipes.add(tp2.pipe_body)
        pipes.add(tp2.pipe_end)

        # ---------------- Terceiro pipe ---------------- #
        # Terceiro LowerPipe
        lp3 = LowerPipe(2)
        pipes.add(lp3.pipe_body)
        pipes.add(lp3.pipe_end)

        # Terceiro TopPipe
        tp3 = TopPipe(lp3.tamanho, 2)
        pipes.add(tp3.pipe_body)
        pipes.add(tp3.pipe_end)

        # Lista contendo as hitbox dos pipes
        rects_pipes = []
        for sprite in pipes.sprites():
            rects_pipes.append(sprite.hitbox)

    for event in pygame.event.get():
        if  event.type == birdImage_troca and not bird.game_over:
            if frame == 0:
                bird.image_original = birdImage_f1
                bird.image = bird.image_original
                frame = 1
            else:
                bird.image_original = birdImage_f2
                bird.image = bird.image_original
                frame = 0
                birdImage_f2, birdImage = birdImage, birdImage_f2
        if event.type == w_troca:
            w_p, w_b = w_b, w_p
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not menu:
            if event.key == pygame.K_w:
                bird.move_up = True
                if not start:
                    start = True

    # Limitar FPS em 60
    dt = clock.tick(60) / 1000

    # Controle de transição
    if fade_in:
        alpha += 255
        if alpha >= 255:
            alpha = 255
            fade_in = False
            fade_out = True
    elif fade_out:
        alpha -= 10
        if alpha <= 0:
            alpha = 0
            fade_out = False

    # Chamar o update() caso o jogo não esteja em estado de game over
    if not bird.game_over:
        if start:
            spritePlayer.update()
            pipes.update()
            tp1.update()
            lp1.update()
            tp2.update()
            lp2.update()
            tp3.update()
            lp3.update()
        bg_x1 -= 2

    if not menu:
        # Somar +1 na pontuação ao passar de um pipe
        if lp1.pipe_body.rect.centerx <= screen.get_width()/4 and conta_pontos == 0:
            sfx_ponto.play()
            score = str(int(score)+1)
            conta_pontos = 1

        # Somar +1 na pontuação ao passar de um pipe
        if lp2.pipe_body.rect.centerx <= screen.get_width()/4 and conta_pontos == 1:
            sfx_ponto.play()
            score = str(int(score)+1)
            conta_pontos = 2

        # Somar +1 na pontuação ao passar de um pipe
        if lp3.pipe_body.rect.centerx <= screen.get_width()/4 and conta_pontos == 2:
            sfx_ponto.play()
            score = str(int(score)+1)
            conta_pontos = 0

        # Mudar o posicionamento do primeiro pipe após passar da tela
        if lp1.pipe_body.rect.right <= 0:
            lp1.kill()
            tp1.kill()
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            lp1 = LowerPipe(lp3.pipe_body.rect.left+220)
            pipes.add(lp1.pipe_body)
            pipes.add(lp1.pipe_end)
            tp1 = TopPipe(lp1.tamanho, lp3.pipe_body.rect.left+220)
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
            lp2 = LowerPipe(lp1.pipe_body.rect.left+220)
            pipes.add(lp2.pipe_body)
            pipes.add(lp2.pipe_end)
            tp2 = TopPipe(lp2.tamanho, lp1.pipe_body.rect.left+220)
            pipes.add(tp2.pipe_body)
            pipes.add(tp2.pipe_end)
            rects_pipes.append(lp2.pipe_body)
            rects_pipes.append(lp2.pipe_end)
            rects_pipes.append(tp2.pipe_body)
            rects_pipes.append(tp2.pipe_end)

        # Mudar o posicionamento do terceiro pipe após passar da tela
        if lp3.pipe_body.rect.right <= 0:
            lp3.kill()
            tp3.kill()
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            rects_pipes.pop(0)
            lp3 = LowerPipe(lp2.pipe_body.rect.left+220)
            pipes.add(lp3.pipe_body)
            pipes.add(lp3.pipe_end)
            tp3 = TopPipe(lp3.tamanho, lp2.pipe_body.rect.left+220)
            pipes.add(tp3.pipe_body)
            pipes.add(tp3.pipe_end)
            rects_pipes.append(lp3.pipe_body)
            rects_pipes.append(lp3.pipe_end)
            rects_pipes.append(tp3.pipe_body)
            rects_pipes.append(tp3.pipe_end)

        # Colisão
        if bird.game_over == False and pygame.Rect.collidelist(bird.hitbox, rects_pipes) != -1:
            bird.game_over = True
            sfx_hit.play()

    # Reseta a posição do fundo para a imagem ficar em looping
    if bg_x1 <= -300:
        bg_x1 = 0

    # ---------------- Desenhos ---------------- #
    # Desenhar o BackGround do jogo
    screen.blit(background, (0, 0))
    screen.blit(background_ground, (bg_x1, 580))

    # Desenhar os canos na tela
    pipes.draw(screen)

    # Desenhar o Bird na tela
    screen.blit(bird.image, bird.rect_rotated)

    # Desenhar botão indicativo de iniciar o jogo
    if not start and not menu:
        screen.blit(w_b, (screen.get_width()/2 - 32, screen.get_height()/2))
        screen.blit(getready, (screen.get_width()/5 - 15, screen.get_height()/6))
        bird.rect.center = (screen.get_width()/4, screen.get_height()/2)
        bird.rect_rotated.center = (screen.get_width()/4, screen.get_height()/2)
    # Desenhar o score
    elif start and not bird.game_over:
        score_text = fonte_numero.render(score, False, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(screen.get_width()/2, screen.get_height()/10))
        screen.blit(score_text, score_text_rect)

    if menu:
        # Título Flappy Bird
        screen.blit(flappybird, (screen.get_width()/8, screen.get_height()/3 - 36 + title_x))
        bird.rect_rotated.center = (screen.get_width() - screen.get_width()/6 + 20, screen.get_height()/3 + title_x)

        # Botão de Start
        screen.blit(button_start, (screen.get_width()/6, screen.get_height() - screen.get_height()/5 + 10))

        # Botão de Quit
        screen.blit(button_quit, (250, screen.get_height() - screen.get_height()/5 + 10))

        # Checagem de clicar no Start
        if pygame.mouse.get_pressed()[0]:
            if button_start.get_rect(left=screen.get_width()/6, top=screen.get_height() - screen.get_height()/5 + 10).collidepoint(pygame.mouse.get_pos()):
                fade_in = True
                sfx_alterna_aba.play()
                bird.reset()
                menu = False
        
        # Checagem de clicar no Quit
        if pygame.mouse.get_pressed()[0]:
            if button_quit.get_rect(left=250, top=screen.get_height() - screen.get_height()/5 + 10).collidepoint(pygame.mouse.get_pos()):
                running = False

        if title_x >= 20:
            title_sobe = True
        elif title_x <= -20:
            title_sobe = False

        if title_sobe:    
            title_x -= 1
        else:
            title_x += 1

    # Imprimir tela de game over
    if bird.game_over:
        bird.update()
        
        # Nome GameOver
        screen.blit(gameover, (screen.get_width()/5 - 15, screen.get_height()/4))

        # Painel
        screen.blit(painel, (screen.get_width()/5 - 40, screen.get_height()/3 + 50))

        # Medalha
        if int(score) >= 10 and int(score) < 20:
            screen.blit(medalha_bronze, (screen.get_width()/5 - 15, screen.get_height()/3 + 105))
        elif int(score) >= 20 and int(score) < 40:
            screen.blit(medalha_silver, (screen.get_width()/5 - 15, screen.get_height()/3 + 105))
        elif int(score) >= 40:
            screen.blit(medalha_gold, (screen.get_width()/5 - 15, screen.get_height()/3 + 105))

        # Textos do painel
        # MEDAL
        medal_text = fonte_menu_panel.render("MEDAL", False, (231, 76, 60))
        medal_text_rect = medal_text.get_rect(left = screen.get_width()/5, top=screen.get_height()/3 + 80)
        screen.blit(medal_text, medal_text_rect)

        # SCORE
        score_text2 = fonte_menu_panel.render("SCORE", False, (231, 76, 60))
        score_text2_rect = score_text2.get_rect(left = screen.get_width()/2 + 60, top=screen.get_height()/3 + 80)
        screen.blit(score_text2, score_text2_rect)

        # BEST
        best_text = fonte_menu_panel.render("BEST", False, (231, 76, 60))
        best_text_rect = best_text.get_rect(left = screen.get_width()/2 + 70, top=screen.get_height()/3 + 150)
        screen.blit(best_text, best_text_rect)

        # botão OK
        screen.blit(button_ok, (screen.get_width()/3 + 18, screen.get_height()/2 + 130))

        # Checagem de clicar no OK
        if pygame.mouse.get_pressed()[0]:
            if button_ok.get_rect(left=screen.get_width()/3 + 18, top=screen.get_height()/2 + 130).collidepoint(pygame.mouse.get_pos()):
                fade_in = True
                sfx_alterna_aba.play()
                restart = True
                bird.image = birdImage
                bird.rect.center = (screen.get_width()/4, screen.get_height()/2)
                bird.rect_rotated = bird.image.get_rect()
        
        # Desenhar o número do Score atual
        score_text = fonte_numero.render(score_animation, False, (0, 0, 0))
        score_text_rect = score_text.get_rect(left = screen.get_width()/2 + 85, top=screen.get_height()/3 + 100)
        screen.blit(score_text, score_text_rect)


        # Salvar HighScore em arquivo
        if int(score) > highscr:
            highscr = int(score)
            with open("scr.bin", "wb") as arquivo:
                scr_bin = json.dumps(int(score)).encode("utf-8")
                arquivo.write(scr_bin)

        # Desenhar o número do Best Score
        highscore_text = fonte_numero.render(highscore_animation, False, (0, 0, 0))
        highscore_text_rect = highscore_text.get_rect(left = screen.get_width()/2 + 85, top=screen.get_height()/3 + 170)
        screen.blit(highscore_text, highscore_text_rect)

        if int(score_animation) < int(score):
            score_animation = str(int(score_animation) + 1)
        
        if int(highscore_animation) < highscr:
            highscore_animation = str(int(highscore_animation) + 1)

    # Aplicar a opacidade na superfície de fade
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))

    # Desenhos das hitbox para teste
    #pygame.draw.rect(screen, (100, 0, 0), bird.hitbox, 2)      # Hitbox do pássaro

    #pygame.draw.rect(screen, (0, 0, 255), lp1.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), lp1.pipe_end.hitbox, 2)
    #pygame.draw.rect(screen, (0, 0, 255), tp1.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), tp1.pipe_end.hitbox, 2)

    #pygame.draw.rect(screen, (0, 0, 255), lp2.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), lp2.pipe_end.hitbox, 2)
    #pygame.draw.rect(screen, (0, 0, 255), tp2.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), tp2.pipe_end.hitbox, 2)
        
    #pygame.draw.rect(screen, (0, 0, 255), lp3.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), lp3.pipe_end.hitbox, 2)
    #pygame.draw.rect(screen, (0, 0, 255), tp3.pipe_body.hitbox, 2)
    #pygame.draw.rect(screen, (100, 100, 255), tp3.pipe_end.hitbox, 2)

    # Atualizar tela
    pygame.display.flip()


pygame.quit()