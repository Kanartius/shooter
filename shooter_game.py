import pygame
import random
import time

WINDOW_SIZE = (700, 500)
FPS = 60
MAX_ENEMIES = 10
ENEMY_SPAWN_TIME = 2000  # Время в миллисекундах между появлениями врагов

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Космическая Игра")

pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("fire.ogg")

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, WINDOW_SIZE)

font = pygame.font.Font(None, 36)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, position, scale):
        super().__init__()
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (
            int(original_image.get_width() * scale),
            int(original_image.get_height() * scale)
        ))
        self.rect = self.image.get_rect(topleft=position)

class Player(GameSprite):
    def __init__(self, position):
        super().__init__("rocket.png", position, scale=0.1)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_SIZE[0]:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def __init__(self):
        x = random.randint(0, WINDOW_SIZE[0] - 60)
        super().__init__("ufo.png", (x, -60), scale=0.1)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_SIZE[1]:
            self.rect.y = -60
            self.rect.x = random.randint(0, WINDOW_SIZE[0] - self.rect.width)
        return self.rect.top > WINDOW_SIZE[1]

class Bullet(GameSprite):
    def __init__(self, position):
        super().__init__("bullet.png", position, scale=0.05)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

def main():
    clock = pygame.time.Clock()
    running = True
    player = Player((350, 400))

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    all_sprites.add(player)
    score_misses = 0
    score_hits = 0
    last_enemy_spawn_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet((player.rect.centerx, player.rect.top))
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.kill()
                    score_hits += 1

        if pygame.sprite.spritecollide(player, enemies, False):
            running = False

        for enemy in enemies:
            if enemy.update():
                score_misses += 1

        if score_misses >= 3:
            running = False
        if score_hits >= 10:
            running = False

        current_time = pygame.time.get_ticks()
        if (current_time - last_enemy_spawn_time) >= ENEMY_SPAWN_TIME and len(enemies) < MAX_ENEMIES:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            last_enemy_spawn_time = current_time

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        misses_text = font.render(f'Пропущенные: {score_misses}', True, (255, 255, 255))
        hits_text = font.render(f'Сбитые: {score_hits}', True, (255, 255, 255))
        screen.blit(misses_text, (10, 10))
        screen.blit(hits_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    if score_hits >= 10:
        print("Вы выиграли! Сбитые враги: ", score_hits)
    else:
        print("Вы проиграли! Пропущенные враги: ", score_misses)

if __name__ == "__main__":
    main() 