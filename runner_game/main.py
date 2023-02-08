# consult readme if necessary
import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):  # player inherits the sprite class
    def __init__(self):  # any time a player object is created, we want it to do something immediately
        super().__init__()  # initializing the sprite class within this class

        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,311))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and self.rect.bottom >= 311:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity = self.gravity + 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 311:
            self.rect.bottom = 311

    def animation_shift(self):
        if self.rect.bottom < 311:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_shift()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):  # the type argument will represent either the snail or the fly obstacle
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_position = 200
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_position = 311

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_position))

    def animation_shift(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_shift()
        self.rect.x -= 5
        self.destroy()
        # if collision_sprite():
        #     pass

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(str(current_time // 1000), False, 'orange').convert()
    score_rectangle = score_surface.get_rect(midtop = text_rectangle.midbottom)
    screen.blit(score_surface, score_rectangle)
    return current_time // 1000


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):  # sprite, obstacle, destroy obstacle?
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
# core variables
screen = pygame.display.set_mode((800, 400))  # (width, height), where origin is at the top left
pygame.display.set_caption("running game")  # window title
clock = pygame.time.Clock()  # handles framerate and time
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # (font type (none = default), font size)
game_on = False  # game state variable
start_time = 0
player_score = 0

# sound
bgm = pygame.mixer.Sound('audio/music.wav')
bgm.set_volume(0.1)
bgm.play(loops= -1)

# player
player = pygame.sprite.GroupSingle()
player.add(Player())  # adds instance of player sprite

# obstacles
obstacle_group = pygame.sprite.Group()


# surfaces, rectangles
sky_surface = pygame.image.load('graphics/Sky.png').convert()  # dimensions = (800,300)
ground_surface = pygame.image.load('graphics/ground.png')  # dimensions = (800,168)

text_surface = test_font.render(' how long can you last', False, (64,64,64)).convert()  # (text to display, anti-alias? = True if you want edges smoothed out, color)
text_rectangle = text_surface.get_rect(center= (400,50))

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()  # these will display on game start/game over
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, -45, 2)
player_stand_rectangle = player_stand_surface.get_rect(center=(400,200))

game_title_font_surface = test_font.render('this is a running game',False, (111,196,169)).convert()
game_title_rectangle = game_title_font_surface.get_rect(midtop=(400,50))

game_start_instruction_surface = test_font.render('press space to start', False, (111,196,169)).convert()
game_start_instruction_rectangle = game_start_instruction_surface.get_rect(midtop=(400,300))

game_controls_instruction_surface = test_font.render('press space to jump', False, (111,196,169)).convert()
game_controls_instruction_rectangle = game_start_instruction_surface.get_rect(midtop= game_start_instruction_rectangle.midbottom)


# custom events - pygame limitations dictate up to 9
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  # milliseconds

# this loop will run forever, otherwise it will terminate after one frame
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_on == False:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                game_on = True
                start_time = pygame.time.get_ticks()

        # spawning obstacles
        if event.type == obstacle_timer and game_on == True:
            obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    # main game loop
    if game_on == True:
        screen.blit(sky_surface, (0,0))  # surface variable name, x-y position, where (0,0) is the origin at the top left.
        screen.blit(ground_surface, (0, 300))

        pygame.draw.rect(screen, 0xc0e8ec, text_rectangle, border_top_left_radius=10, border_bottom_right_radius=10)

        screen.blit(text_surface, text_rectangle)

        player_score = display_score()

        # PLAYER
        player.draw(screen)  # takes only one argument
        player.update()

        # OBSTACLE
        obstacle_group.draw(screen)
        obstacle_group.update()

        # COLLISIONS
        game_on = collision_sprite()

    else:  # post-game/menu screen
        screen.fill((94,129,162))
        screen.blit(game_title_font_surface,game_title_rectangle)
        screen.blit(player_stand_surface, player_stand_rectangle)

        if player_score == 0:  # if it's the player's first time running the file, display the title screen
            screen.blit(game_start_instruction_surface, game_start_instruction_rectangle)
            screen.blit(game_controls_instruction_surface, game_controls_instruction_rectangle)

        else:  # otherwise, display the game over screen
            previous_score_font_surface = test_font.render('previous score: ' + str(player_score), False, (111, 196, 169))
            previous_score_rectangle = previous_score_font_surface.get_rect(midtop=(400, 300))
            screen.blit(previous_score_font_surface,previous_score_rectangle)

    pygame.display.update()
    clock.tick(60)  # framerate ceiling
