import pygame


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image


class Player:
    def __init__(self, screen, isRight):
        BLACK = (0, 0, 0)
        self.screen = screen
        self.idle = True
        self.walking = False
        self.crouch = False
        self.isRight = isRight

        self.jumping = False
        self.vel_y = 20

        self.x = 0
        self.y = 0

        # idle animation
        self.idle_animation_step = 10
        self.idle_animation_cooldown = 100
        self.idle_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_Idle.png').convert_alpha())
        self.idle_animation = [self.idle_sprite_sheet.get_image(i, 120, 80, 5, BLACK) for i in
                               range(self.idle_animation_step)]
        self.idle_animation_frame = 0

        # walk animation
        self.walk_animation_step = 10
        self.walk_animation_cooldown = 100
        self.walk_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_Run.png').convert_alpha())
        self.walk_animation = [self.walk_sprite_sheet.get_image(i, 120, 80, 5, BLACK) for i in
                               range(self.walk_animation_step)]
        self.walk_animation_frame = 0

        # crouch
        self.crouch_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_Crouch.png').convert_alpha())
        self.crouch_idle = self.crouch_sprite_sheet.get_image(0, 120, 80, 5, BLACK)

        # jump
        self.jump_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_JumpFallInbetween.png').convert_alpha())
        self.jump_up = self.jump_sprite_sheet.get_image(0, 120, 80, 5, BLACK)
        self.jump_down = self.jump_sprite_sheet.get_image(1, 120, 80, 5, BLACK)

    def update(self):
        if self.idle:
            self.walk_animation_frame = 0
            self.idle_animation_frame += 1
            if self.idle_animation_frame == len(self.idle_animation):
                self.idle_animation_frame = 0

        if self.walking:
            self.idle_animation_frame = 0
            self.walk_animation_frame += 1
            if self.walk_animation_frame == len(self.walk_animation):
                self.walk_animation_frame = 0

        if self.jumping:
            self.y -= self.vel_y * 5
            self.vel_y -= 10
            if self.vel_y < -20:
                self.jumping = False
                self.vel_y = 20
                self.y = 0

    def draw(self):
        if self.idle:
            self.screen.blit(
                pygame.transform.flip(self.idle_animation[self.idle_animation_frame], flip_x=not self.isRight,
                                      flip_y=False), (self.x, self.y))
        if self.walking:
            self.screen.blit(
                pygame.transform.flip(self.walk_animation[self.walk_animation_frame], flip_x=not self.isRight,
                                      flip_y=False), (self.x, self.y))
        if self.crouch:
            self.screen.blit(
                pygame.transform.flip(self.crouch_idle, flip_x=not self.isRight, flip_y=False), (self.x, self.y))

        if self.jumping:
            if self.vel_y > 0:
                self.screen.blit(
                    pygame.transform.flip(self.jump_up, flip_x=not self.isRight, flip_y=False), (self.x, self.y))
            else:
                self.screen.blit(
                    pygame.transform.flip(self.jump_down, flip_x=not self.isRight, flip_y=False), (self.x, self.y))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(
                             self.x + 250, self.y + 200 + (80 if self.crouch else 0),
                             100, 200 - (80 if self.crouch else 0)), 1
                         )

    def move(self):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if not self.jumping and pygame.KEYDOWN and key[pygame.K_w]:
            self.jumping = True
        if key[pygame.K_a]:
            dx = -2
            self.isRight = False
            self.walking = True
            self.idle = False
            self.crouch = False
        elif key[pygame.K_d]:
            dx = 2
            self.isRight = True
            self.walking = True
            self.idle = False
            self.crouch = False
        elif key[pygame.K_s]:
            self.walking = False
            self.idle = False
            self.crouch = True
        else:
            self.walking = False
            self.idle = True
            self.crouch = False
        self.x += dx
        self.y += dy
