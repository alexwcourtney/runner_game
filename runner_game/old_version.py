# consult readme if necessary
import pygame
from sys import exit
from random import randint

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(str(current_time // 1000), False, 'orange').convert()
    score_rectangle = score_surface.get_rect(midtop = text_rectangle.midbottom)
    # print(current_time // 1000)
    screen.blit(score_surface, score_rectangle)
    return current_time // 1000

def obstacle_movement(obstacle_list):
    if obstacle_list: # evaluates True if list has 1+ items
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x = obstacle_rectangle.x - 5 # move the given obstacle 5 px to the left
               # newlist = [expression for item in iterable if condition == True]

            if obstacle_rectangle.bottom == 311:
                screen.blit(snail_surface, obstacle_rectangle)
            else:
                screen.blit(fly_surface, obstacle_rectangle)


            #screen.blit(snail_surface, obstacle_rectangle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right >= 0]
        return obstacle_list # we need to return this so that the variables within are accessible anywhere
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle): return False
    return True

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 311: # is the player in the air?
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    # play walking animation if player's on the ground
    # display the jump surface when the player is in the air

# init MUST be run before any other pygame functionality can work
pygame.init()
# create a display surface, as a variable - this is basically the game window
screen = pygame.display.set_mode((800, 400)) # (width, height)
# set window title
pygame.display.set_caption("running game")
# initialize a clock to help handle framerate and time
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #(font type (none = default), font size)
game_on = False # this will be the game state. If game over, the value will be False
start_time = 0
player_score = 0
player_gravity = 0

# surfaces, rectangles
sky_surface = pygame.image.load('graphics/Sky.png').convert() # dimensions = (800,300)

ground_surface = pygame.image.load('graphics/ground.png') # dimensions = (800,168)

text_surface = test_font.render(' how long can you last', False, (64,64,64)).convert() # (text to display, anti-alias? = True if you want edges smoothed out, color)
text_rectangle = text_surface.get_rect(center= (400,50))

game_over_surface = test_font.render('game over, brah', False, (64,64,64)).convert()
game_over_rectangle = game_over_surface.get_rect(midbottom = (400, 200))


# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # removes the image's alpha value, allowing for transparency behind the image
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# fly
fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 # this will index the above the list for animation purposes
player_jump = pygame.image.load('graphics/player/jump.png')

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,311)) #takes the player surface, draws a rectangle around it. Note that the rectangle coords replace the need for explicit coords in the BLIT

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, -45, 2)
player_stand_rectangle = player_stand_surface.get_rect(center=(400,200))

game_title_font_surface = test_font.render('this is a running game',False, (111,196,169)).convert()
game_title_rectangle = game_title_font_surface.get_rect(midtop=(400,50))

game_start_instruction_surface = test_font.render('press space to start', False, (111,196,169)).convert()
game_start_instruction_rectangle = game_start_instruction_surface.get_rect(midtop=(400,300))

game_controls_instruction_surface = test_font.render('press space to jump', False, (111,196,169)).convert()
game_controls_instruction_rectangle = game_start_instruction_surface.get_rect(midtop= game_start_instruction_rectangle.midbottom)

# previous_score_font_surface = test_font.render('previous score: ' + str(player_score), False, (111,196,169))
# previous_score_rectangle = previous_score_font_surface.get_rect(midtop= (400,300))

#custom events - you can only have 9 or so due to pygame limitations
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) # milliseconds

#animation timers
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 10)

# this loop will run forever, otherwise it will terminate after one frame
while True:
    # check for player input, called the "event loop"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.quit un-initializes pygame
            pygame.quit()
            exit() # imported from sys
        if game_on == True:
            if event.type == pygame.KEYDOWN:
                # print(pygame.key.name(event.key))
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 311:
                    print('jump man now please thank you')
                    player_gravity = -20
                # if pygame.key.name(event.key) == 'space':
                #     print('jump man please jump omg')
                if game_on == False:
                    if event.key == pygame.K_RETURN:
                        game_on = True

            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 311: # checking for button input first before looking for collisions are more efficient
                if player_rectangle.collidepoint(event.pos):
                    print('ok')
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                print('game over, enter OR spacebar pressed')
                game_on = True
                #snail_rectangle.left = 800
                start_time = pygame.time.get_ticks()

    # draw all of our elements
    # update everything
    # if they overlap, surfaces will display on top of one another if they are initiated in order

        if event.type == obstacle_timer and game_on == True:
            print('obstacles in the list: ' + str(len(obstacle_rectangle_list)))
            if randint(0,2) == True:
                #snail
                obstacle_rectangle_list.append(snail_surface.get_rect(midbottom=((randint(900, 1100)), 311)))
            else:
                #fly
                obstacle_rectangle_list.append(fly_surface.get_rect(midbottom=((randint(900,1100),100))))

        if event.type == snail_animation_timer and game_on == True:
            if snail_frame_index == 0:
                snail_frame_index = 1
            else:
                snail_frame_index = 0
            snail_surface = snail_frames[snail_frame_index]

        if event.type == fly_animation_timer and game_on == True:
            if fly_frame_index == 0:
                fly_frame_index = 1
            else:
                fly_frame_index = 0
            fly_surface = fly_frames[fly_frame_index]




    if game_on == True:

        screen.blit(sky_surface, (0,0)) # surface variable name, x-y position, where (0,0) is the origin at the top left.
        screen.blit(ground_surface, (0, 300))

        pygame.draw.rect(screen, 0xc0e8ec, text_rectangle, border_top_left_radius=10, border_bottom_right_radius=10)

        screen.blit(text_surface, text_rectangle)
        # screen.blit(score_surface, score_rectangle)
        player_score = display_score()

        #snail_rectangle.left = snail_rectangle.left - 5

        #PLAYER
        player_gravity = player_gravity + 1
        player_rectangle.top = player_rectangle.top + player_gravity
        player_animation()
        screen.blit(player_surface, player_rectangle)
        #screen.blit(snail_surface, snail_rectangle)

        # if snail_rectangle.right <= 0:
        #     snail_rectangle.left = 800

        if player_rectangle.bottom > 310:
            player_rectangle.bottom = 311
            player_gravity = 0

        # obstacle movement
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        #collisions
        game_on = collisions(player_rectangle, obstacle_rectangle_list)

    else: # post-game/menu screen
        screen.fill((94,129,162))
        screen.blit(game_title_font_surface,game_title_rectangle)
        screen.blit(player_stand_surface, player_stand_rectangle)
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80,311)
        player_gravity = 0


        if player_score == 0:
            screen.blit(game_start_instruction_surface, game_start_instruction_rectangle)
            screen.blit(game_controls_instruction_surface, game_controls_instruction_rectangle)




        else:
            #screen.blit(previous_score_font_surface,previous_score_rectangle)
            previous_score_font_surface = test_font.render('previous score: ' + str(player_score), False, (111, 196, 169))
            previous_score_rectangle = previous_score_font_surface.get_rect(midtop=(400, 300))
            screen.blit(previous_score_font_surface,previous_score_rectangle)
       #  screen.blit(game_over_surface, game_over_rectangle)

    pygame.display.update()
    clock.tick(60) # this sets a framerate ceiling, our game is simple enough that we won't need a floor

# rectangles allow for us to grab a position at various key/important coordinates of a given image
# rectangle positions in a tuple: topleft, midtop, topright, midleft, center, midright, bottomleft, midbottom, bottomright
# individual values: x,y, top, left, centerx, centery, right, bottom