import pygame
import time
import random
import sys
import time

from PIL import Image, ImageSequence


def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
    return frames

class AnimatedSpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, bottom, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = (x, bottom))
        self.image_index = 0

    def update(self):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1500
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

ground = dis.get_height()

gifFrameList = loadGIF('frame_0_delay-0.1s.gif')
animated_sprite = AnimatedSpriteObject(dis.get_width() // 2, ground, gifFrameList)
all_sprites = pygame.sprite.Group(animated_sprite)

gifFrameList_light = loadGIF('frame_0_delay-0.1s.gif')
animated_sprite_light = AnimatedSpriteObject(dis.get_width() // 2, ground, gifFrameList_light)
all_sprites_light = pygame.sprite.Group(animated_sprite_light)

start_menu = True

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load(r"WhatsApp Image 2024-01-02 at 6.28.11 PM.jpeg").convert()
        self.x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        self.y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        self.y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        return self.x, self.y

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 3, dis_height / 2])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    apple = Apple(dis)
    foodx, foody = apple.move()

    direction = 'RIGHT'
    change_to = direction

    while not game_over:

        while game_close == True:
            all_sprites.update()
            all_sprites.draw(dis)
            pygame.display.flip()
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
            clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            y1_change = -snake_block
            x1_change = 0
        if direction == 'DOWN':
            y1_change = snake_block
            x1_change = 0
        if direction == 'LEFT':
            x1_change = -snake_block
            y1_change = 0
        if direction == 'RIGHT':
            x1_change = snake_block
            y1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)

        apple.draw()
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            all_sprites_light.update()
            all_sprites_light.draw(dis)
            pygame.display.flip()
            pygame.display.update()
            time.sleep(0.2)
            foodx, foody = apple.move()
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


while start_menu:

    all_sprites.update()
    all_sprites.draw(dis)
    pygame.display.flip()
    quit_message = font_style.render('Press S to Start', True, black)
    dis.blit(quit_message, [dis_width / 2, dis_height / 2.5])
    quit_message = font_style.render('Press Q to Quit', True, black)
    dis.blit(quit_message, [dis_width / 2, dis_height / 2])
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                gameLoop()
            if event.key == pygame.K_q:
                sys.exit()

    clock.tick(10)