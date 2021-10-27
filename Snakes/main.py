import pygame
import time
import random
from PIL import Image,ImageFilter

pygame.init()

SCREENHEIGHT = 400
SCREENWIDTH = 600
FPS = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Snakes by Varad")
clock = pygame.time.Clock()

pygame.mixer.music.set_volume(0.7)
#Loading sounds and images:-
GAME_IMAGES = {}
GAME_SOUNDS = {}
GAME_IMAGES["Background"] = pygame.image.load("Imgs/background.jpg").convert_alpha()
GAME_SOUNDS["Eat"] = pygame.mixer.Sound("Sounds/Eat1.wav")
GAME_IMAGES["Welcome"] = pygame.image.load("Imgs/WelcomeScreen1.jpg").convert_alpha()
GAME_IMAGES["Paused"] = pygame.image.load("Imgs/Paused1.jpg").convert_alpha()
GAME_SOUNDS["Die"] = pygame.mixer.Sound("Sounds/Die1.wav")
GAME_SOUNDS["Music"] = pygame.mixer.music.load("Sounds/Music.wav")
GAME_IMAGES["Food"] = pygame.image.load("Imgs/food.png").convert_alpha()
GAME_IMAGES["G_Food"] = pygame.image.load("Imgs/Golden food.png").convert_alpha()
GAME_IMAGES["GameOver"] = pygame.image.load("Imgs/GameOver1.jpg").convert_alpha()
GAME_IMAGES["Numbers"] = (
    pygame.image.load("Imgs/0.png").convert_alpha(),
    pygame.image.load("Imgs/1.png").convert_alpha(),
    pygame.image.load("Imgs/2.png").convert_alpha(),
    pygame.image.load("Imgs/3.png").convert_alpha(),
    pygame.image.load("Imgs/4.png").convert_alpha(),
    pygame.image.load("Imgs/5.png").convert_alpha(),
    pygame.image.load("Imgs/6.png").convert_alpha(),
    pygame.image.load("Imgs/7.png").convert_alpha(),
    pygame.image.load("Imgs/8.png").convert_alpha(),
    pygame.image.load("Imgs/9.png").convert_alpha()
)

def game_overf():
    GAME_SOUNDS["Die"].play()
    hiscore_list = [int(num) for num in list(str(content))]
    score_list = [int(num) for num in list(str(score))]
    time.sleep(1)
    while True:
        x = 300
        X = 300
        SCREEN.blit(GAME_IMAGES["GameOver"],(0,0))
        for char in score_list:
            SCREEN.blit(GAME_IMAGES["Numbers"][char],(x,135))
            x += GAME_IMAGES["Numbers"][char].get_width()
        for charr in hiscore_list:
            SCREEN.blit(GAME_IMAGES["Numbers"][charr],(X,200))
            X += GAME_IMAGES["Numbers"][charr].get_width()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and (event.key != pygame.K_UP and event.key != pygame.K_DOWN and event.key != pygame.K_RIGHT and event.key != pygame.K_LEFT):
                return

def WelcomeS():
    pygame.mixer.music.play()
    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        SCREEN.blit(GAME_IMAGES["Welcome"],(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def test_collide(snake_pres):
    others = snake_pres[:-1]
    main = snake_pres[-1]
    for X,Y in others:
        if X == main[0] and Y == main[1]:
            return True

def draw_snake(window,color,snake_pres):
    for x,y in snake_pres:
        global snake
        snake = pygame.Rect(x,y,15,15)
        pygame.draw.rect(SCREEN,(137, 24, 24),snake)

def main_game():
    global GAME_IMAGES
    global score
    global content
    #Snake Variables:-
    x = 0
    y = 0
    vel = 1
    activeVar = "Down"
    body = []
    head = []
    snake_length = 1

    #Food Variables:-
    foodX = random.randint(10,SCREENWIDTH)
    foodY = random.randint(40,SCREENHEIGHT)
    food_on_screen = False

    #Golden Food Variables:-
    G_foodX = random.randint(10,SCREENWIDTH)
    G_foodY = random.randint(40,SCREENHEIGHT)
    food_on_screen = False
    requirment = random.randint(4,16)
    req = 0
    current = ""
    f = pygame.font.SysFont("lucida",60)

    game_paused = False
    game_over = False
    score = 0
    font = pygame.font.SysFont("lucida",40)

    pygame.mixer.music.set_volume(0.2)
    previous_var = time.time()
    count = 6
    while not game_over:
        if not game_paused:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            SCREEN.blit(GAME_IMAGES["Background"],(0,0))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE):
                    game_paused = True

            if keys[pygame.K_UP] and not activeVar == "Down":
                activeVar = "Up"

            elif keys[pygame.K_DOWN] and not activeVar == "Up":
                activeVar = "Down"

            elif keys[pygame.K_RIGHT] and not activeVar == "Left":
                activeVar = "Right"

            elif keys[pygame.K_LEFT] and not activeVar == "Right":
                activeVar = "Left"
            
            if activeVar == "Up":
                y -= vel
            
            if activeVar == "Down":
                y += vel

            if activeVar == "Left":
                x -= vel

            if activeVar == "Right":
                x += vel

            if x >= SCREENWIDTH + 1:
                x = -1

            if x < -1:
                x = SCREENWIDTH + 1

            if y < -2:
                y = SCREENHEIGHT + 2

            if y > SCREENHEIGHT + 2:
                y = -2

            SCREEN.blit(GAME_IMAGES["Background"],(0,0))
            head.clear()
            head.append(x)
            head.append(y)
            body.append(head.copy())

            if len(body) > snake_length:
                del body[0]

            draw_snake(SCREEN,(137, 24, 24),body)

            if test_collide(body):
                game_over = True
                return

            if food_on_screen:
                if food.colliderect(snake):
                    count = 6
                    snake_length += 10
                    req += 1
                    if current == "Golden":
                        score += 30
                    else:
                        score += 5
                    with open("hiscores.txt") as file:
                        content = int(file.read().strip())
                    if content < score:
                        with open("hiscores.txt","w") as file:
                            file.write(str(score))
                    with open("hiscores.txt") as file:
                        content = int(file.read().strip())
                    GAME_SOUNDS["Eat"].play()
                    if req == requirment:
                        G_foodX = random.randint(10,SCREENWIDTH-50)
                        G_foodY = random.randint(40,SCREENHEIGHT-50)
                        current = "Golden"
                        req = 0
                        requirment = random.randint(4,16)
                    else:
                        current = "Normal"
                        foodX = random.randint(10,SCREENWIDTH-50)
                        foodY = random.randint(40,SCREENHEIGHT-50)

                if current == "Golden":
                    if (time.time()-previous_var) > 1:
                        count -= 1
                        if count <= 0:
                            count = 6
                            current = "Normal"
                            req = 0
                        previous_var = time.time()
                    countdown = f.render(str(count),True,(241, 255, 142))
                    SCREEN.blit(countdown,(SCREENWIDTH-50,20))

                if current == "Golden":
                    food = pygame.Rect(G_foodX,G_foodY,30,30)
                    SCREEN.blit(GAME_IMAGES["G_Food"],food)
                else:
                    food = pygame.Rect(foodX,foodY,30,30)
                    SCREEN.blit(GAME_IMAGES["Food"],food)

                text = font.render(f"Score:{score}",True,(0,0,0))
                SCREEN.blit(text,(10,10))
                pygame.display.update()
            else:
                food = pygame.Rect(foodX,foodY,10,10)
                pygame.draw.rect(SCREEN,(220,52,52),food)
                pygame.display.update()
                food_on_screen = True

            clock.tick(FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE):
                    game_paused = False
            
            pygame.image.save(SCREEN,"Temporary.png")
            back_img = Image.open("Temporary.png")
            blurred = back_img.filter(ImageFilter.GaussianBlur(4))
            blurred.save("Temporary.png")
            
            SCREEN.blit(pygame.image.load("Temporary.png").convert_alpha(),(0,0))
            SCREEN.blit(GAME_IMAGES["Paused"],(112,70))
            pygame.display.update()

if __name__ == "__main__":
    WelcomeS()
    while True:
        main_game()
        game_overf()