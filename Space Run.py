import sys
import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(topleft = (100,420))
        self.gravity = 0
        self.player_jump = pygame.image.load('jump.png').convert_alpha()


    def animation_stage(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -30

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 500:
            self.rect.bottom = 500

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_stage()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly1 = pygame.image.load('Fly1.png').convert_alpha()
            fly2 = pygame.image.load('Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 170
        else:
            snail = pygame.image.load('snail1.png').convert_alpha()
            snail2 = pygame.image.load('snail2.png').convert_alpha()
            self.frames = [snail, snail2]
            y_pos = 470
        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (random.randint(1280,1400),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 10
        self.destroy()





def display_score():
    current_time = round((pygame.time.get_ticks()/1000) - start_time)
    timer = word.render("score: " + str(current_time),False,(64,64,64))
    timer_rect = timer.get_rect(center = (640,80))
    screen.blit(timer,timer_rect)
    return current_time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Snail Jump")
clock = pygame.time.Clock()
score = 0
start_time = 0

# word
word = pygame.font.Font(None, 50)
text = word.render("Space Runner", False, (64,64,64))
text_rect = text.get_rect(center = (640,120))

text2 = word.render("Press space to play", False, (64,64,64))
text_rect2 = text2.get_rect(center = (640,600))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

def player_animation():
    global player, player_index
    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

# Groups
new_player = pygame.sprite.GroupSingle()
new_player.add(Player())

obstacle_group = pygame.sprite.Group()

player_walk1 = pygame.image.load('player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('jump.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0

player = player_walk[0]
player_rect = player.get_rect(topleft = (100,420))


player_gravity = 0
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(250,300))
player_stand_rect = player_stand_scaled.get_rect(center = (640,360))

# snail
snail = pygame.image.load('snail1.png').convert_alpha()
snail_rect = snail.get_rect(topleft = (1280,470))
snail2 = pygame.image.load('snail2.png').convert_alpha()
snail_frames = [snail,snail2]
snail_frame_index = 0
default_snail = snail_frames[snail_frame_index]

# fly
fly1 = pygame.image.load('Fly1.png').convert_alpha()
fly2 = pygame.image.load('Fly2.png').convert_alpha()
fly_frames = [fly1,fly2]
fly_frame_index = 0
default_fly = fly_frames[fly_frame_index]

obstacle_rect_list = []
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            if obstacle_rect.y == 170:
                screen.blit(default_fly,obstacle_rect)
            else:
                screen.blit(default_snail,obstacle_rect)
        obstacle_list = [obstacle_rect for obstacle_rect in obstacle_list if obstacle_rect.x > -100]
        return obstacle_list
    else:
        return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(new_player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


# background
surface = pygame.image.load('Sky.png').convert()
sky = pygame.transform.scale(surface,(1280,720))
surface2 = pygame.image.load('ground.png').convert()
ground = pygame.transform.scale(surface2,(1280,300))

# snail settings
speed = 4

running = False

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE and player_rect.bottom == 500:
                    player_gravity = -30
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -30

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    start_time = (pygame.time.get_ticks()/1000)

        if running:

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(random.choice(['fly','snail','snail'])))

                #if random.randint(0,2):
                    #obstacle_rect_list.append(snail.get_rect(topleft = (random.randint(1280,1400),470)))
                #else:
                    #obstacle_rect_list.append(fly1.get_rect(topleft = (random.randint(1280,1400),170)))

            elif event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                default_snail = snail_frames[snail_frame_index]

            elif event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                default_fly = fly_frames[fly_frame_index]

    if running:
        #snail_rect.left -= speed
        #if snail_rect.right <= 0:
            #snail_rect.x =  1300
            #speed = speed * 1.2
        #player_rect.left += 1

        score = display_score()
        text3 = word.render("Your score is " + str(score), False, (64, 64, 64))
        text_rect3 = text2.get_rect(center=(640, 630))

        if player_rect.colliderect(snail_rect):
            running = False
        mouse_pos = pygame.mouse.get_pos()

    # positions
        screen.fill("black")
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,500))
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #running = collision(player_rect,obstacle_rect_list)
        running = collision_sprite()

        #player_rect.y += player_gravity
        #player_gravity += 1
        #if player_rect.bottom > 500:
            #player_rect.bottom = 500
        #player_animation()
        #screen.blit(player,player_rect)
        new_player.draw(screen)
        new_player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()


        display_score()

    else:
        obstacle_rect_list.clear()
        player_rect.topleft = (100,420)
        screen.fill((64,129,162))
        screen.blit(player_stand_scaled,player_stand_rect)
        screen.blit(text,text_rect)
        screen.blit(text2, text_rect2)
        if score > 0:
            screen.blit(text3,text_rect3)


    pygame.display.update()
    clock.tick(60)

pygame.quit()



