import tkinter as tk
import pygame
import pygame.draw

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('PyBlock')
    screen.fill((0, 0, 0))

    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)

    pygame.draw.circle(s, (255, 255, 255, 255), (100, 100), 5)

    screen.blit(s, (0, 0))
    pygame.display.flip()

    try:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
