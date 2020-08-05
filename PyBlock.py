import sys
import pygame

ScreenSize   = 640,480

BrickW   = 60
BrickH  = 15
PaddleW  = 60
PaddleH = 12
BallDiameter = 16
BallRadius   = BallDiameter*0.5

MaxXRangePaddle = ScreenSize[0] - PaddleW
MaxXRangeBALL   = ScreenSize[0] - BallDiameter
MaxYRangeBALL   = ScreenSize[1] - BallDiameter

PADDLE_Y = ScreenSize[1] - PaddleH - 10

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
GOLD = (200,200,0)
GREEN = (0,255,0)
SKY_BLUE = (0,239,255)
ORANGE = (255,154,0)
RED = (255,0,0)

STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
STATE_NEXT_LEVEL = 4
STATE_PAUSE = 5

class PyBlock:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_caption("PyBlock by Aayush Gandhi")
        
        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None
        self.lives = 3
        self.level = 1
        self.score = 0
        self.Paddle_Speed = 18

        self.init_game()

        
    def init_game(self):
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PaddleW,PaddleH)
        self.ball     = pygame.Rect(300,PADDLE_Y - BallDiameter,BallDiameter,BallDiameter)

        if self.level == 1:
            self.ball_vel = [5,-5]
        elif self.level == 2:
            self.ball_vel = [6,-6]
        elif self.level == 3:
            self.ball_vel = [7,-7]
        elif self.level == 4:
            self.ball_vel = [8,-8]
        else:
            self.ball_vel = [9,-9]

        self.create_bricks()
        

    def create_bricks(self):
            y_ofs = 35
            self.bricks = []
            for i in range(7):
                x_ofs = 35
                for j in range(8):
                    self.bricks.append(pygame.Rect(x_ofs,y_ofs,BrickW,BrickH))
                    x_ofs += BrickW + 10
                y_ofs += BrickH + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, self.BRICK_COLOUR, brick)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.paddle.left -= self.Paddle_Speed
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += self.Paddle_Speed
            if self.paddle.left > MaxXRangePaddle:
                self.paddle.left = MaxXRangePaddle

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = self.ball_vel
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and self.state == STATE_NEXT_LEVEL:
            self.level += 1
            self.init_game()
            self.Difficulty()
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()
            self.lives = 3
            self.score = 0
            self.level = 1
            self.Paddle_Speed = 20
            self.ball_vel = [5,-5]

        if len(self.bricks) == 0:
            self.state = STATE_NEXT_LEVEL

        if keys[pygame.K_SPACE] and self.ball.top > self.paddle.top:
            if self.state == STATE_GAME_OVER and self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER
                    
    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MaxXRangeBALL:
            self.ball.left = MaxXRangeBALL
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MaxYRangeBALL:            
            self.ball.top = MaxYRangeBALL
            self.ball_vel[1] = -self.ball_vel[1]

    def CollisionHandling(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                if self.BRICK_COLOUR == GOLD:
                    self.score += 3
                elif self.BRICK_COLOUR == RED:
                    self.score += 5
                elif self.BRICK_COLOUR == SKY_BLUE:
                    self.score += 8
                elif self.BRICK_COLOUR == ORANGE:
                    self.score += 10
                else:
                    self.score += (self.level*5)
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BallDiameter
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            elif self.lives == 0 and self.score >= 1500:
                self.state = STATE_WON
            elif self.lives == 0 and self.score < 1500:
                self.state = STATE_GAME_OVER

    def Difficulty(self):
        if self.level == 2:
            self.Paddle_Speed = 16
            self.ball_vel = [6,-6]
            self.lives += 1
        elif self.level == 3:
            self.Paddle_Speed = 14
            self.ball_vel = [7,-7]
            self.lives += 2
        elif self.level == 4:
            self.Paddle_Speed = 12
            self.ball_vel = [8,-8]
            self.lives += 3
        else:
            self.Paddle_Speed = 10
            self.ball_vel = [9,-9]
            self.lives += 4

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives) + " LEVEL: " + str(self.level), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (ScreenSize[0] - size[0]) / 2
            y = (ScreenSize[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
        
            
    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

            self.clock.tick(50)
            self.screen.fill(BLACK)
            self.check_input()
            
            if self.level == 1:
                self.BRICK_COLOUR = GOLD
            elif self.level == 2:
                self.BRICK_COLOUR = SKY_BLUE
            elif self.level == 3:
                self.BRICK_COLOUR = ORANGE
            elif self.level == 4:
                self.BRICK_COLOUR = RED
            else:
                self.BRICK_COLOUR = GREEN

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.CollisionHandling()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_NEXT_LEVEL:
                self.show_message("YOU WON THIS LEVEL! PRESS TO CONTINUE")
                
            self.draw_bricks()
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            pygame.draw.circle(self.screen, WHITE, (int(self.ball.left + BallRadius),int(self.ball.top + BallRadius)),int(BallRadius))

            self.show_stats()

            pygame.display.flip()

try:
    if __name__ == "__main__":
        PyBlock().run()
except:
    print("The game has quit successfully! Thanks for playing")
