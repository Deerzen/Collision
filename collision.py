import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()
window_size = [800, 600]
FPS = 60
score = 0
winner = 0
colors = {
    "yellow": (245, 173, 88),
    "red": (217, 94, 64),
    "green": (86, 188, 138),
    "purple": (167, 125, 194),
    "white": (246, 246, 246),
    "black": (29, 24, 24),
}

confirm = pygame.mixer.Sound(os.path.join(sys.path[0], "Sound/impact.wav"))
speed_up = pygame.mixer.Sound(os.path.join(sys.path[0], "Sound/MENU A_Select.wav"))
speed_down = pygame.mixer.Sound(os.path.join(sys.path[0], "Sound/MENU A - Back.wav"))
points = pygame.mixer.Sound(os.path.join(sys.path[0], "Sound/MENU_Pick.wav"))
lose = pygame.mixer.Sound(os.path.join(sys.path[0], "Sound/MENU B_Back.wav"))

window = pygame.display.set_mode((window_size[0], window_size[1]))
pygame.display.set_caption("Collision")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 20)


def text_objects(text, font):
    textSurface = font.render(text, True, colors["black"])
    return textSurface, textSurface.get_rect()


def shuffle_location() -> list:
    return [random.randint(50, 750), random.randint(50, 550)]


# logic for player movement
def player_movement(player, stats, block_size) -> list:
    current_stats = stats
    controls = {
        1: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN],
        2: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
    }
    keys = pygame.key.get_pressed()
    if keys[controls[player][0]] and current_stats[0] > 0:
        current_stats[0] -= current_stats[2]
    if keys[controls[player][1]] and current_stats[0] + block_size / 2 < window_size[0]:
        current_stats[0] += current_stats[2]
    if keys[controls[player][2]] and current_stats[1] > 0:
        current_stats[1] -= current_stats[2]
    if keys[controls[player][3]] and current_stats[1] + block_size / 2 < window_size[1]:
        current_stats[1] += current_stats[2]
    return current_stats


# button function
def button(msg, x, y, w, h, ic, ac, action=None):
    multiplayer_mode = 0

    if msg == "1 Player":
        multiplayer_mode = False

    elif msg == "2 Players":
        multiplayer_mode = True

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            confirm.play()
            if action != game_menu:
                action(multiplayer_mode)
            else:
                action()

    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (int(x + (w / 2)), int(y + (h / 2)))
    window.blit(textSurf, textRect)


# menu function
def game_menu():
    block_size = 20
    velocity = [4, 4]
    posm_x = 400
    posm_y = 300
    pygame.mixer.music.load(os.path.join(sys.path[0], "Sound/menu.ogg"))
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

        if posm_x + block_size > window_size[0] or posm_x < 0:
            velocity[0] = -velocity[0]
        if posm_y + block_size > window_size[1] or posm_y < 0:
            velocity[1] = -velocity[1]

        window.fill(colors["white"])
        pygame.draw.rect(
            window, colors["black"], [posm_x, posm_y, block_size, block_size]
        )
        largeText = pygame.font.Font("freesansbold.ttf", 100)
        TextSurf, TextRect = text_objects("Collision", largeText)
        TextRect.center = (int(window_size[0] / 2), int(window_size[1] / 2))
        window.blit(TextSurf, TextRect)
        pygame.mouse.get_pos()
        score = 0

        button(
            "1 Player",
            150,
            450,
            100,
            50,
            colors["green"],
            colors["yellow"],
            game_loop,
        )
        button(
            "2 Players",
            550,
            450,
            100,
            50,
            colors["red"],
            colors["yellow"],
            game_loop,
        )
        pygame.display.update()
        clock.tick(60)


# game-loop function
def game_loop(multiplayer_mode):
    block_size = 20
    velocities = {
        0: [2, 2],
        1: [3, 3],
        2: [4, 4],
        3: [-2, -2],
        4: [-3, -3],
        5: [-4, -4],
    }
    block_locations = {
        0: [400, 300],
        1: [200, 150],
        2: [500, 300],
        3: [100, 500],
        4: [300, 400],
        5: [50, 200],
    }
    point_locations = {
        0: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
        1: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
        2: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
        3: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
    }
    item_locations = {
        0: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
        1: [
            random.randint(50, window_size[0] - 50),
            random.randint(50, window_size[1] - 50),
        ],
    }

    # x/y coordinates & speed for player 1 and 2
    player1_stats = [window_size[0] / 8, window_size[1] / 6, 3]
    if multiplayer_mode:
        player2_stats = [window_size[0] / 4, window_size[1] / 3, 3]

    pygame.mixer.music.load(os.path.join(sys.path[0], "Sound/theme.ogg"))
    pygame.mixer.music.play(-1)

    # game-loop
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

        player1_stats = player_movement(1, player1_stats, block_size)
        if multiplayer_mode:
            player2_stats = player_movement(2, player2_stats, block_size)

        # DRAW
        window.fill(colors["black"])

        playa = pygame.draw.rect(
            window,
            colors["yellow"],
            [
                player1_stats[0],
                player1_stats[1],
                block_size / 2,
                block_size / 2,
            ],
        )
        if multiplayer_mode:
            playa1 = pygame.draw.rect(
                window,
                colors["red"],
                [
                    player2_stats[0],
                    player2_stats[1],
                    block_size / 2,
                    block_size / 2,
                ],
            )

        for i, value in block_locations.items():
            block = pygame.draw.rect(
                window,
                colors["white"],
                [
                    block_locations[i][0],
                    block_locations[i][1],
                    block_size,
                    block_size,
                ],
            )

            value[0] += velocities[i][0]
            block_locations[i][1] += velocities[i][1]
            if (
                block_locations[i][0] + block_size > window_size[0]
                or block_locations[i][0] < 0
            ):
                velocities[i][0] = -velocities[i][0]
            if (
                block_locations[i][1] + block_size > window_size[1]
                or block_locations[i][1] < 0
            ):
                velocities[i][1] = -velocities[i][1]

            if multiplayer_mode:
                if playa.colliderect(block):
                    if player1_stats[2] != 0:
                        lose.play()
                    player1_stats[2] = 0
                if playa1.colliderect(block):
                    if player2_stats[2] != 0:
                        lose.play()
                    player2_stats[2] = 0
                if player1_stats[2] == 0 and player2_stats[2] == 0:
                    if score1 > score2:
                        score = score1
                        return return_score(1, multiplayer_mode, score)
                    if score2 > score1:
                        score = score2
                        return return_score(2, multiplayer_mode, score)
                    if score1 == score2:
                        return return_score(0, multiplayer_mode, score)
            elif playa.colliderect(block):
                lose.play()
                you_lose(multiplayer_mode)
                return score
        for i in point_locations:
            point = pygame.draw.rect(
                window,
                colors["green"],
                [
                    point_locations[i][0],
                    point_locations[i][1],
                    block_size / 2,
                    block_size / 2,
                ],
            )

            if multiplayer_mode:
                if playa.colliderect(point):
                    score1 += 5
                    point_locations[i] = shuffle_location()
                    points.play()
                if playa1.colliderect(point):
                    score2 += 5
                    point_locations[i] = shuffle_location()
                    points.play()
            elif playa.colliderect(point):
                score += 5
                point_locations[i] = shuffle_location()
                points.play()

        for i in item_locations:
            item = pygame.draw.rect(
                window,
                colors["purple"],
                [
                    item_locations[i][0],
                    item_locations[i][1],
                    block_size / 2,
                    block_size / 2,
                ],
            )

            if playa.colliderect(item):
                flip = random.randint(0, 1)
                if flip == 0:
                    player1_stats[2] += 1
                    speed_up.play()
                elif flip == 1 and player1_stats[2] >= 2:
                    player1_stats[2] -= 1
                    speed_down.play()

                item_locations[0] = shuffle_location()
                item_locations[1] = shuffle_location()

            if multiplayer_mode and playa1.colliderect(item):
                flip = random.randint(0, 1)
                if flip == 0:
                    player2_stats[2] += 1
                    speed_up.play()
                elif flip == 1 and player2_stats[2] >= 2:
                    player2_stats[2] -= 1
                    speed_down.play()

                item_locations[0] = shuffle_location()
                item_locations[1] = shuffle_location()

        pygame.display.update()
        clock.tick(FPS)

        if not multiplayer_mode:
            label = myfont.render(f"Your score is: {str(score)}", 1, colors["red"])
            window.blit(label, (10, 10))
            label = myfont.render(
                f"Current player1_stats[2]: {str(player1_stats[2])}", 1, colors["red"]
            )

            window.blit(label, (670, 10))
        else:
            label = myfont.render(f"Score Player 1: {str(score1)}", 1, colors["yellow"])
            window.blit(label, (10, 10))
            label = myfont.render(f"Score Player 2: {str(score2)}", 1, colors["red"])
            window.blit(label, (10, 25))
            label = myfont.render(
                f"player1_stats[2] Player 1: {str(player1_stats[2])}",
                1,
                colors["yellow"],
            )

            window.blit(label, (670, 10))
            label = myfont.render(
                f"player1_stats[2] Player 2: {str(player2_stats[2])}", 1, colors["red"]
            )

            window.blit(label, (670, 25))
        pygame.display.flip()

        pygame.event.pump()


def return_score(arg0, multiplayer_mode, score):
    winner = arg0
    you_lose(multiplayer_mode)
    return score


def you_lose(is_multiplayer):
    global score
    ending = True
    pygame.mixer.music.load(os.path.join(sys.path[0], "Sound/ulose.ogg"))
    pygame.mixer.music.play(-1)

    while ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(colors["white"])
        largeText = pygame.font.Font("freesansbold.ttf", 40)
        if not is_multiplayer:
            TextSurf, TextRect = text_objects(
                f"Your final score is {str(score)}", largeText
            )

        elif winner == 1:
            TextSurf, TextRect = text_objects(
                f"Player 1 wins with {str(score)} points", largeText
            )

        elif winner == 2:
            TextSurf, TextRect = text_objects(
                f"Player 2 wins with {str(score)} points", largeText
            )

        else:
            TextSurf, TextRect = text_objects("Draw", largeText)

        TextRect.center = (int(window_size[0] / 2), int(window_size[1] / 2))
        window.blit(TextSurf, TextRect)

        pygame.mouse.get_pos()

        # button menu
        button(
            "Back",
            window_size[0] / 2 - 50,
            450,
            100,
            50,
            colors["yellow"],
            colors["green"],
            game_menu,
        )

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    game_menu()
