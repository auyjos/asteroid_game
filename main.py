import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot


def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    
    
    #initialize the asteroid field and player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and not player.alive():
                if event.key == pygame.K_SPACE:
                    # Clear all sprite groups
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    
                    # Create new player and asteroid field
                    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                    asteroid_field = AsteroidField()
                    score = 0

        
        screen.fill("black")

        if player.alive():
            updatable.update(dt)
        
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game Over")
                    player.kill()
                    break
                for shot in shots:
                    if shot.collides_with(asteroid):
                        shot.kill()
                        # Add score based on asteroid size
                        if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
                            score += SCORE_LARGE      # Large asteroid (60 radius)
                        elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                            score += SCORE_MEDIUM     # Medium asteroid (40 radius)
                        else:
                            score += SCORE_SMALL      # Small asteroid (20 radius)
                        asteroid.split()
                        break

            for sprite in drawable:
                sprite.draw(screen)

            draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH // 2, 20)
        else:
            # Draw game over screen
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
            draw_text(screen, f"Final Score: {score}", 48, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
            draw_text(screen, "Press SPACE to restart", 36, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80)


        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
