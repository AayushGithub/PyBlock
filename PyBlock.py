import pygame

ScreenSize= 640,480

class PyBlock:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption("PyBlock")
        
        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

try:
    if __name__ == "__main__":
        PyBlock().run()
except:
    print("PyBlock has quit successfully! Thanks for playing!")
