import pygame
import time
import random
import sys
import shelve
import os

pygame.init()
pygame.mixer.init()

window_w = 800
window_h = 600

yellow = (245, 173, 88)
red = (217, 94, 64)
green = (86, 188, 138)
purple = (167, 125, 194)
white = (246, 246, 246)
black = (29, 24, 24)

FPS = 10

score = 0
winner = 0

confirm = pygame.mixer.Sound(os.path.join(sys.path[0], "impact.wav"))
speed_up = pygame.mixer.Sound(os.path.join(sys.path[0], "MENU A_Select.wav"))
speed_down = pygame.mixer.Sound(os.path.join(sys.path[0], "MENU A - Back.wav"))
points = pygame.mixer.Sound(os.path.join(sys.path[0], "MENU_Pick.wav"))
lose = pygame.mixer.Sound(os.path.join(sys.path[0], "MENU B_Back.wav"))

window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Collision")
clock = pygame.time.Clock()

myfont = pygame.font.SysFont("monospace", 20)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


#button function
def button(msg,x,y,w,h,ic,ac,action=None):
    multiplayer_mode = 0

    if msg == "1 Player":
        multiplayer_mode = False
    elif msg == "2 Players":
        multiplayer_mode = True

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            confirm.play()
            if action != game_menu:
                action(multiplayer_mode)
            else:
                action()

    else:
        pygame.draw.rect(window, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)


#menu function
def game_menu():
    block_size = 20
    velocity = [4, 4]
    posm_x = 400
    posm_y = 300
    pygame.mixer.music.load(os.path.join(sys.path[0],"menu.ogg"))
    pygame.mixer.music.play(-1)

    global score
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit(0)
                quit()

        posm_x += velocity[0]
        posm_y += velocity[1]

        if posm_x + block_size > window_w or posm_x < 0:
            velocity[0] = -velocity[0]

        if posm_y + block_size > window_h or posm_y < 0:
            velocity[1] = -velocity[1]

        window.fill(white)
        pygame.draw.rect(window, black, [posm_x, posm_y, block_size, block_size])
        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("Collision", largeText)
        TextRect.center = ((window_w/2),(window_h/2))
        window.blit(TextSurf, TextRect)

        pygame.mouse.get_pos()

        score = 0

        button("1 Player",150,450,100,50,green,yellow,game_loop)
        button("2 Players", 550,450,100,50,red,yellow,game_loop)

        pygame.display.update()
        clock.tick(60)


#game-loop function
def game_loop(multiplayer_mode):
    block_size = 20
    #velocity = [2, 2]
    #velocity1 = [3, 3]
    #velocity2 = [4, 4]
    #velocity3 = [-2, -2]
    #velocity4 = [-3, -3]
    #velocity5 = [-4, -4]

    velocities = {
                    0: [2, 2],
                    1: [3, 3],
                    2: [4, 4],
                    3: [-2, -2],
                    4: [-3, -3],
                    5: [-4, -4]
                    }
    print(velocities)

    #position-blöcke
    #pos_x = 400
    #pos_y = 300

    #pos1_x = 200
    #pos1_y = 150

    #pos2_x = 500
    #pos2_y = 300

    #pos3_x = 100
    #pos3_y = 500

    #pos4_x = 300
    #pos4_y = 400

    #pos5_x = 50
    #pos5_y = 200

    #block locations
    block_locations = {
                        0: [400, 300],
                        1: [200, 150],
                        2: [500, 300],
                        3: [100, 500],
                        4: [300, 400],
                        5: [50, 200]
                        }
    print(block_locations)


    #position-points
    posp_x = random.randint(50,750)
    posp_y = random.randint(50,550)

    posp1_x = random.randint(50,750)
    posp1_y = random.randint(50,550)

    posp2_x = random.randint(50,750)
    posp2_y = random.randint(50,550)

    posp3_x = random.randint(50,750)
    posp3_y = random.randint(50,550)

    #position-items
    posit_x = random.randint(50,750)
    posit_y = random.randint(50,550)

    posit1_x = random.randint(50,750)
    posit1_y = random.randint(50,550)

    #position-player
    posi_x = window_w/8
    posi_y = window_h/6
    speed = 3

    #position-player2
    if multiplayer_mode:
        posi1_x = window_w/4
        posi1_y = window_h/3
        speed1 = 3

    pygame.mixer.music.load(os.path.join(sys.path[0],"theme.ogg"))
    pygame.mixer.music.play(-1)

    #game-loop
    running = True
    global score
    if multiplayer_mode:
        global winner
        score1 = 0
        score2 = 0


    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                quit()



        for i in block_locations:

            block_locations[i][0] += velocities[i][0]
            block_locations[i][1] += velocities[i][1]

            if block_locations[i][0] + block_size > window_w or block_locations[i][0] < 0:
                velocities[i][0] = -velocities[i][0]
            if block_locations[i][1] + block_size > window_h or block_locations[i][1] < 0:
                velocities[i][1] = -velocities[i][1]







        #player-movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if posi_x > 0:
                posi_x -= speed
        if keys[pygame.K_RIGHT]:
            if posi_x + block_size/2 < window_w:
                posi_x += speed
        if keys[pygame.K_UP]:
            if posi_y > 0:
                posi_y -= speed
        if keys[pygame.K_DOWN]:
            if posi_y + block_size/2 < window_h:
                posi_y += speed


        #player-movement2
        if multiplayer_mode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if posi1_x > 0:
                    posi1_x -= speed1
            if keys[pygame.K_d]:
                if posi1_x + block_size/2 < window_w:
                    posi1_x += speed1
            if keys[pygame.K_w]:
                if posi1_y > 0:
                    posi1_y -= speed1
            if keys[pygame.K_s]:
                if posi1_y + block_size/2 < window_h:
                    posi1_y += speed1


        # DRAW
        window.fill(black)

        b1 = pygame.draw.rect(window, white, [block_locations[0][0], block_locations[0][1], block_size, block_size])
        b2 = pygame.draw.rect(window, white, [block_locations[1][0], block_locations[1][1], block_size, block_size])
        b3 = pygame.draw.rect(window, white, [block_locations[2][0], block_locations[2][1], block_size, block_size])
        b4 = pygame.draw.rect(window, white, [block_locations[3][0], block_locations[3][1], block_size, block_size])
        b5 = pygame.draw.rect(window, white, [block_locations[4][0], block_locations[4][1], block_size, block_size])
        b6 = pygame.draw.rect(window, white, [block_locations[5][0], block_locations[5][1], block_size, block_size])

        p1 = pygame.draw.rect(window, green, [posp_x, posp_y, block_size/2, block_size/2])
        p2 = pygame.draw.rect(window, green, [posp1_x, posp1_y, block_size/2, block_size/2])
        p3 = pygame.draw.rect(window, green, [posp2_x, posp2_y, block_size/2, block_size/2])
        p4 = pygame.draw.rect(window, green, [posp3_x, posp3_y, block_size/2, block_size/2])

        i1 = pygame.draw.rect(window, purple, [posit_x, posit_y, block_size/2, block_size/2])
        i2 = pygame.draw.rect(window, purple, [posit1_x, posit1_y, block_size/2, block_size/2])

        playa = pygame.draw.rect(window, yellow, [posi_x, posi_y, block_size/2, block_size/2])
        if multiplayer_mode:
            playa1 = pygame.draw.rect(window, red, [posi1_x, posi1_y, block_size/2, block_size/2])

        #update score
        if playa.colliderect(p1):
            if multiplayer_mode == False:
                score += 5
            else:
                score1 += 5
            posp_x = random.randint(50,750)
            posp_y = random.randint(50,550)
            points.play()
        if playa.colliderect(p2):
            if multiplayer_mode == False:
                score += 5
            else:
                score1 += 5
            posp1_x = random.randint(50,750)
            posp1_y = random.randint(50,550)
            points.play()
        if playa.colliderect(p3):
            if multiplayer_mode == False:
                score += 5
            else:
                score1 += 5
            posp2_x = random.randint(50,750)
            posp2_y = random.randint(50,550)
            points.play()
        if playa.colliderect(p4):
            if multiplayer_mode == False:
                score += 5
            else:
                score1 += 5
            posp3_x = random.randint(50,750)
            posp3_y = random.randint(50,550)
            points.play()

        #update score 2
        if multiplayer_mode:
            if playa1.colliderect(p1):
                score2 += 5
                posp_x = random.randint(50,750)
                posp_y = random.randint(50,550)
                points.play()
            if playa1.colliderect(p2):
                score2 += 5
                posp1_x = random.randint(50,750)
                posp1_y = random.randint(50,550)
                points.play()
            if playa1.colliderect(p3):
                score2 += 5
                posp2_x = random.randint(50,750)
                posp2_y = random.randint(50,550)
                points.play()
            if playa1.colliderect(p4):
                score2 += 5
                posp3_x = random.randint(50,750)
                posp3_y = random.randint(50,550)
                points.play()


        #item behavior
        if playa.colliderect(i1):
            speed += 1
            posit_x = random.randint(50,750)
            posit_y = random.randint(50,550)
            posit1_x = random.randint(50,750)
            posit1_y = random.randint(50,550)
            speed_up.play()

        if playa.colliderect(i2):
            if speed >= 2:
                speed -= 1
            if multiplayer_mode == False:
                if score >= 5:
                    score -= 5
            else:
                if score1 >= 5:
                    score1 -= 5

            posit_x = random.randint(50,750)
            posit_y = random.randint(50,550)
            posit1_x = random.randint(50,750)
            posit1_y = random.randint(50,550)
            speed_down.play()

        if multiplayer_mode:
            if playa1.colliderect(i1):
                speed1 += 1
                posit_x = random.randint(50,750)
                posit_y = random.randint(50,550)
                posit1_x = random.randint(50,750)
                posit1_y = random.randint(50,550)
                speed_up.play()
            if playa1.colliderect(i2):
                if speed1 >= 2:
                    speed1 -= 1
                elif score2 >= 5:
                    score2 -= 5
                posit_x = random.randint(50,750)
                posit_y = random.randint(50,550)
                posit1_x = random.randint(50,750)
                posit1_y = random.randint(50,550)
                speed_down.play()


        #losing-condition
        if multiplayer_mode == False:
            if playa.colliderect(b1) or playa.colliderect(b2) or playa.colliderect(b3) or playa.colliderect(b4) or playa.colliderect(b5) or playa.colliderect(b6):
                lose.play()
                you_lose(multiplayer_mode)
                return score

        else:
            if playa.colliderect(b1) or playa.colliderect(b2) or playa.colliderect(b3) or playa.colliderect(b4) or playa.colliderect(b5) or playa.colliderect(b6):
                if speed != 0:
    	            lose.play()
                speed = 0
            if playa1.colliderect(b1) or playa1.colliderect(b2) or playa1.colliderect(b3) or playa1.colliderect(b4) or playa1.colliderect(b5) or playa1.colliderect(b6):
                if speed1 != 0:
    	            lose.play()
                speed1 = 0
            if speed == 0 and speed1 == 0:
                if score1 > score2:
                    score = score1
                    winner = 1
                    you_lose(multiplayer_mode)
                    return score
                if score2 > score1:
                    score = score2
                    winner = 2
                    you_lose(multiplayer_mode)
                    return score
                if score1 == score2:
                    winner = 0
                    you_lose(multiplayer_mode)
                    return score

        pygame.display.update()
        clock.tick(FPS)

        if multiplayer_mode == False:
            label = myfont.render("Your score is: " + str(score), 1, red)
            window.blit(label, (10, 10))

            label = myfont.render("Current Speed: " + str(speed), 1, red)
            window.blit(label, (670, 10))

            pygame.display.flip()

        else:
            label = myfont.render("Score Player 1: " + str(score1), 1, yellow)
            window.blit(label, (10, 10))
            label = myfont.render("Score Player 2: " + str(score2), 1, red)
            window.blit(label, (10, 25))
            label = myfont.render("Speed Player 1: " + str(speed), 1, yellow)
            window.blit(label, (670, 10))
            label = myfont.render("Speed Player 2: " + str(speed1), 1, red)
            window.blit(label, (670, 25))
            pygame.display.flip()


def you_lose(is_multiplayer):

    global score
    ending = True

    pygame.mixer.music.load(os.path.join(sys.path[0],"ulose.ogg"))
    pygame.mixer.music.play(-1)

    while ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',40)
        if is_multiplayer == False:
            TextSurf, TextRect = text_objects("Your final score is " + str(score), largeText)
        else:
            if winner == 1:
                TextSurf, TextRect = text_objects("Player 1 wins with " + str(score) + " points", largeText)
            elif winner == 2:
                TextSurf, TextRect = text_objects("Player 2 wins with " + str(score) + " points", largeText)
            else:
                TextSurf, TextRect = text_objects("Draw", largeText)

        TextRect.center = ((window_w/2),(window_h/2))
        window.blit(TextSurf, TextRect)

        pygame.mouse.get_pos()

        #button menu
        button("Back",window_w/2-50,450,100,50,yellow,green,game_menu)

        pygame.display.update()
        clock.tick(15)

game_menu()
