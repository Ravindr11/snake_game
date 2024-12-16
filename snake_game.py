import pygame
import random

x = pygame.init()
print(x)

# --------------- Game variables ------------------

# Full screen info
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_hight = screen_info.current_h

gameWindow = pygame.display.set_mode((screen_width, screen_hight), pygame.FULLSCREEN)

padding = int(0.014*screen_hight)
border = 2

# score area
score_area_width = screen_width - 2*padding
score_area_hight = int(0.1*screen_hight)

# Play ground size
play_ground_width = screen_width - 2*padding
play_ground_hight = screen_hight - score_area_hight - 3*padding

# Play ground limits
top_limit = padding + border
bottom_limit = padding + play_ground_hight - border
left_limit = padding + border
right_limit = padding + play_ground_width - border 

game_exit = False
game_over = False

score = 0

snake_x = 300
snake_y = 200
snake_velocity = 5
snake_velocity_x = 5
snake_velocity_y = 0
snake_size = 15
snake_length = 10
snake_list = [[snake_x, snake_y]]

snake_eat_sound = "eat.mp3"
pygame.mixer.init()

food_x = 200
food_y = 200

game_font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
fps = 60

"""In this according to the logic actualy the fps is the velocity and the snake_velocity is fps or I say seems to be fps"""

# -------- Colors ---------
light_green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

food_color = red
bg_color = black
snake_color = white

# All functions
def draw_text(text, color, x, y):
    screen_text = game_font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def eat_food():
    global food_x, food_y, snake_length, snake_list, score, snake_size
    #Deleting the old food
    pygame.draw.rect(gameWindow, bg_color, [food_x, food_y, snake_size, snake_size])

    #Making eat sound
    pygame.mixer.music.load(snake_eat_sound)
    pygame.mixer.music.play()

    #Increasing lenth
    snake_length += 1
    snake_list.insert(0, [100, 100])
    score += 1

    #Score update
    pygame.draw.rect(gameWindow, bg_color, [padding + 20, play_ground_hight + 2*padding + 20, 150, 30])
    draw_text("Score: " + str(score), snake_color, padding + 20, play_ground_hight + 2*padding + 20)
    # draw_text("Level: " + str(score), snake_color, padding + 200, play_ground_hight + 2*padding + 20)

    #Creating a new food
    food_x = random.randint(left_limit + 20, right_limit - 20)
    food_y = random.randint(top_limit + 20, bottom_limit - 20)
    pygame.draw.rect(gameWindow, food_color, [food_x, food_y, snake_size, snake_size])  #FOOD
    
    # Moving forward without deleting tail
    head = [snake_x, snake_y] 
    snake_list.append(head)
    # pygame.draw.rect(gameWindow, snake_color, [snake_x, snake_y, snake_size, snake_size]) 
    del snake_list[0]

def moving_forward():
    """ As the snake is moving forward,
        we are assuming that a new head block is created
        and a tail block is deleted """
        
    global snake_x, snake_y, snake_list, snake_size, gameWindow, snake_color
    head = [snake_x, snake_y] 
    snake_list.append(head)
    pygame.draw.rect(gameWindow, snake_color, [snake_x, snake_y, snake_size, snake_size]) 
    pygame.draw.rect(gameWindow, bg_color, [snake_list[0][0], snake_list[0][1], snake_size, snake_size])
    del snake_list[0]

def init_game():
    """ Filling elements in the game window """
    
    pygame.display.set_caption("Snake Game")
    
    # Play ground
    gameWindow.fill(bg_color)
    pygame.draw.rect(gameWindow, light_green,
                     (padding, padding, play_ground_width, play_ground_hight),
                     border, 10, 10, 10, 10)
    
    # Scoring area
    pygame.draw.rect(gameWindow, yellow,
                     (padding, play_ground_hight + 2*padding, score_area_width, score_area_hight))
    
    pygame.draw.rect(gameWindow, bg_color,
                     (padding + 2, play_ground_hight + 2*padding + 2, score_area_width - 4, score_area_hight - 4))

    draw_text("Score: 0", snake_color, padding + 20, play_ground_hight + 2*padding + 20)
    draw_text("Level: 1", snake_color, padding + 200, play_ground_hight + 2*padding + 20)
    
    #Creating a initial food
    pygame.draw.rect(gameWindow, food_color, [food_x, food_y, snake_size, snake_size])  #FOOD

    # giving the initial length
    for i in range(snake_length):
        moving_forward()
        eat_food()

# def exit_window() 


if __name__ == '__main__':
    init_game()
    
    #creating a game loop
    while not game_exit:
        # This for loop checks all the events, if any
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(event)
                game_exit = True

            # Changing the direction of snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake_velocity_y != 0:
                    snake_velocity_x = snake_velocity
                    snake_velocity_y = 0
                
                elif event.key == pygame.K_LEFT and snake_velocity_y != 0:
                    snake_velocity_x = -snake_velocity
                    snake_velocity_y = 0
                
                elif event.key == pygame.K_UP and snake_velocity_x != 0:
                    snake_velocity_x = 0
                    snake_velocity_y = -snake_velocity
                
                elif event.key == pygame.K_DOWN and snake_velocity_x != 0:
                    snake_velocity_x = 0
                    snake_velocity_y = snake_velocity
                    
                elif event.key == pygame.K_ESCAPE:
                    game_exit = True
                
        # Movement according to velocity
        snake_x += snake_velocity_x
        snake_y += snake_velocity_y

        # Hitting a Wall (game over)
        hit_condition_x = snake_x < left_limit or snake_x > right_limit - snake_size
        hit_condition_y = snake_y < top_limit or snake_y > bottom_limit - snake_size
        if hit_condition_x or hit_condition_y:
            print("GAME OVER")
            game_exit = True

        # Snake eating itself
        if [snake_x, snake_y] in snake_list:
            print("GAME OVER")
            game_exit = True

        # Eating the food
        eat_condition_x = snake_x > food_x - snake_size and snake_x < food_x + snake_size
        eat_condition_y = snake_y > food_y - snake_size and snake_y < food_y + snake_size
        if eat_condition_x and eat_condition_y:
            eat_food()
            continue

        # Moving forward
        moving_forward()

        pygame.display.update()
        clock.tick(fps)

