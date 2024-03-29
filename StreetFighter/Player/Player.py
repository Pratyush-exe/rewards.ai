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
        self.combo_attacking = False
        self.single_attacking = False
        self.isRight = isRight

        self.jumping = False
        self.vel_y = 20

        self.x = 0
        self.y = 0

        self.char_rect = pygame.Rect(250, 200, 100, 200)

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

        # combo_attack
        self.combo_attack_animation_step = 10
        self.combo_attack_animation_cooldown = 100
        self.combo_attack_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_AttackCombo.png').convert_alpha())
        self.combo_attack_animation = [self.combo_attack_sprite_sheet.get_image(i, 120, 80, 5, BLACK) for i in
                                       range(self.combo_attack_animation_step)]
        self.combo_attack_animation_frame = 0

        # single_attack
        self.single_attack_animation_step = 4
        self.single_attack_animation_cooldown = 100
        self.single_attack_sprite_sheet = SpriteSheet(pygame.image.load('./assets/_CrouchAttack.png').convert_alpha())
        self.single_attack_animation = [self.single_attack_sprite_sheet.get_image(i, 120, 80, 5, BLACK) for i in
                                        range(self.single_attack_animation_step)]
        self.single_attack_animation_frame = 0

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
            self.y -= self.vel_y * 6
            self.char_rect.y -= self.vel_y * 6
            self.vel_y -= 10
            if self.vel_y < -20:
                self.jumping = False
                self.vel_y = 20
                self.y = 0

        if self.combo_attacking:
            self.combo_attack_animation_frame += 1
            if self.combo_attack_animation_frame == self.combo_attack_animation_step:
                self.combo_attacking = False
                self.combo_attack_animation_frame = 0

        if self.single_attacking:
            self.single_attack_animation_frame += 1
            if self.single_attack_animation_frame == self.single_attack_animation_step:
                self.single_attacking = False
                self.single_attack_animation_frame = 0

    def draw(self):
        self.char_rect.height = 130 if self.crouch else 200
        if self.crouch:
            self.char_rect.y = 270
        elif not self.jumping and not self.crouch:
            self.char_rect.y = 200

        if self.single_attacking:
            self.char_rect.width = 250
        elif self.combo_attacking:
            self.char_rect.width = 320
        else:
            self.char_rect.width = 100

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

        if self.combo_attacking:
            self.screen.blit(
                pygame.transform.flip(self.combo_attack_animation[self.combo_attack_animation_frame],
                                      flip_x=not self.isRight,
                                      flip_y=False), (self.x, self.y))

        if self.single_attacking:
            self.screen.blit(
                pygame.transform.flip(self.single_attack_animation[self.single_attack_animation_frame],
                                      flip_x=not self.isRight,
                                      flip_y=False), (self.x, self.y))

        temp_x = self.char_rect.x
        if not self.isRight and self.combo_attacking: self.char_rect.x -= 220
        if not self.isRight and self.single_attacking: self.char_rect.x -= 150

        pygame.draw.rect(self.screen, (255, 255, 255), self.char_rect, 1)

        self.char_rect.x = temp_x

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
        elif not self.combo_attacking and key[pygame.K_q]:
            self.combo_attacking = True
        elif not self.single_attacking and key[pygame.K_e]:
            self.single_attacking = True
        else:
            self.walking = False
            self.idle = True
            self.crouch = False
        self.x += dx
        self.y += dy
        self.char_rect.x += dx
        self.char_rect.y += dy
