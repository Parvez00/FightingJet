from superwires import games, color
import pygame
import random

game_window_width = 280
game_window_height = 500
game_background = pygame.image.load("night_back.jpg")
game_background_rect = game_background.get_rect()


class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("oponent-jet.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(game_window_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(3, 8)
        self.health = 100
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > game_window_height + 10:
            self.rect.x = random.randrange(game_window_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(3, 8)
            player.score -= 1

opponents = pygame.sprite.Group()

for i in range(10):
    opponent = Opponent()
    opponents.add(opponent)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player-jet.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect_centerx = 240
        self.rect.bottom = 480
        self.score = 0

    def shoot(self):
        shell = Shell(self.rect.centerx, self.rect.top)
        all_sprites.add(shell)
        shells.add(shell)


class Shell(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -15

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

shells = pygame.sprite.Group()

pygame.init()

screen = pygame.display.set_mode((game_window_width, game_window_height))
pygame.display.set_caption('Air Shooter')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_sprites.add(opponent)

font = pygame.font.SysFont('comicsans', 15, True)
game_over = font.render("Collide!", 1, color.white)

run = True

while run:
    clock.tick(60)

    hits = pygame.sprite.groupcollide(opponents, shells, True,True)
    for hit in hits:
        opponent = Opponent()
        all_sprites.add(opponent)
        opponents.add(opponent)
        player.score += 1
        shells.remove(hit)

    hits = pygame.sprite.spritecollide(player,opponents, False)

    if hits:
        img = font.render('Game Over!!!', True, color.white)        
        text = font.render(f'Score: {player.score}', 1, color.white)
        screen.blit(game_background, game_background_rect)
        screen.blit(text, (180, 30))
        screen.blit(img, (100, 250))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.mouse.get_pressed()

    if pygame.mouse.get_pressed()[0] and len(shells) < 10:
        player.shoot()

    mx, my = pygame.mouse.get_pos()

    if mx < game_window_width:
        player.rect.x = mx

    pygame.mouse.set_visible(False)

    if player.rect.x > game_window_width:
            player.rect.x = -player.rect.x

    all_sprites.update()

    text = font.render(f'Score: {player.score}', 1, color.white)
    screen.blit(game_background, game_background_rect)
    screen.blit(text, (180, 30))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()




