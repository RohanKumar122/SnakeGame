# Modules__________ import pygame
import pygame
import random
import os

# Initialisations
pygame.mixer.init()
pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (50, 0, 90)
blue = (0, 0, 255)
scolor=(255,0,0)

# Console Detais
screen_width = 900
screen_height = 600
hiscore = 0
gameWindow = pygame.display.set_mode((screen_width, screen_height))


# Game console Title
pygame.display.set_caption("Snakes")
pygame.display.update()
clock = pygame.time.Clock()

# Input Backgrounds
bgimg = pygame.image.load("Images/grass.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
overimg = pygame.image.load("Images/game_over.jpg")
overimg = pygame.transform.scale(overimg, (screen_width, screen_height)).convert_alpha()
welcomeimg = pygame.image.load("Images/background5.jpg")
welcomeimg = pygame.transform.scale(welcomeimg, (screen_width, screen_height)).convert_alpha()
uwelcomeimg = pygame.image.load("Images/snakes start.jpg")
uwelcomeimg = pygame.transform.scale(uwelcomeimg, (screen_width, screen_height)).convert_alpha()

# Font Managements
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

#Welcome background & Music
def welcome():
    pygame.mixer.music.load("Sounds/back.mp3")
    pygame.mixer.music.play(100)
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        gameWindow.blit(welcomeimg, (0, 0))
        # text_screen("THE SNAKES", black, 320, 235)
        # text_screen("Press SPACE to Play", black, 255, 280)
        gameWindow.blit(uwelcomeimg, (0, 0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for event in game_loop():
                        pygame.mixer.music.load("Sounds/back.mp3")
                        pygame.mixer.music.play(100)
                    game_loop()
            pygame.display.update()
            clock.tick(60)
           

def game_loop():
    snk_list = []
    snk_length = 1
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 10
    clock = pygame.time.Clock()
    fps = 30
    velocity_x = 0
    velocity_y = 0

    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(30, screen_width/2)
    food_y = random.randint(30, screen_height/2)
    score = 0
    init_velocity = 5

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(overimg, (0, 0))
            
            
            text_screen("Score: "+ str(score), scolor, 390,300)
            text_screen("Hi-Score: "+ str(hiscore), scolor, 345,340)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        welcome()

        else:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        # snake_x=snake_x+10
                        # velocity_x+=10 """""this line increases the speed as much as the button is pressed """""
                        velocity_x = +init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        # snake_x=snake_x-10
                        # velocity_x-=10
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        # snake_y=snake_y-10
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = +init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x) < 6 and abs(snake_y-food_y) < 6:
                # pygame.mixer.music.load("eat.mp3")
                # pygame.mixer.music.play()
                score += 1

                # print("Score: ",score *10)
                food_x = random.randint(30, screen_width/2)
                food_y = random.randint(30, screen_height/2)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) +
                        "    Hi-Score: "+str(hiscore), blue, 5, 5)
            pygame.draw.rect(
                gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # if head in snk_list[:-1]:
            #     continue
            if head in snk_list[:-3]:
                game_over = True
                pygame.mixer.music.load("Sounds/No.mp3")
                pygame.mixer.music.play()

            if snake_x > screen_width or snake_x < 0 or snake_y < 0 or snake_y > screen_height:
                game_over = True
                # print("game_over")
                pygame.mixer.music.load("Sounds/No.mp3")
                pygame.mixer.music.play()

            # pygame.draw.rect(gameWindow, green, [snake_x, snake_y,snake_size,snake_size])
            plot_snake(gameWindow, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


# game_loop()
welcome()
