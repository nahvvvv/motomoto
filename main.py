import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição de constantes
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.25
FLAP_FORCE = -5
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Carregamento de recursos
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 40))

pipe_img = pygame.Surface((50, HEIGHT))
pipe_img.fill((0, 255, 0))

# Classe para o pássaro
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = FLAP_FORCE

# Classe para os obstáculos (tubos)
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect(midtop=(x, HEIGHT // 2))
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Função para gerar um par de obstáculos (tubos)
def create_pipe():
    gap_y = random.randint(150, HEIGHT - 300)
    bottom_pipe = Pipe(WIDTH + 50)
    top_pipe = Pipe(WIDTH + 50)
    bottom_pipe.rect.bottom = gap_y - 100
    top_pipe.rect.top = gap_y + 100
    pipes.add(bottom_pipe)
    pipes.add(top_pipe)
    all_sprites.add(bottom_pipe)
    all_sprites.add(top_pipe)

# Inicialização das sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)

# Contador de frames para geração de obstáculos
frame_count = 0

# Loop principal do jogo
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Atualização
    all_sprites.update()

    # Geração de obstáculos a cada 100 frames
    frame_count += 1
    if frame_count == 100:
        create_pipe()
        frame_count = 0

    # Colisões
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits or bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
        running = False

    # Renderização
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
