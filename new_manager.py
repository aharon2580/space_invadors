import pygame
import new_settings as nst
import new_entities as ent
import random

st = nst.Settings()


class Manager:
    """Manages the game according to the settings"""

    def __init__(self):
        self.screen = pygame.display.set_mode((st.screen_width, st.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.play = False
        self.level = 1
        self.player_image = self.create_image(st.player_image, st.player_size)
        self.enemy_image = self.create_image(st.enemy_image, st.enemy_size)
        self.player_bullet_image = self.create_image(st.player_bullet_image, st.player_bullet_size)
        self.enemy_bullet_image = self.create_image(st.enemy_bullet_image, st.enemy_bullet_size)

    def init_game(self):
        """Preparing the game"""
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()

    def game_loop(self):
        """Sends to splash screen or level loop"""
        if self.play:
            self.level_loop()
        else:
            self.start_level()

    def start_level(self):
        """Displays the splash screen for the current level"""
        pygame.display.set_caption(f'level {self.level}')
        self.back_image = self.create_image(st.back_image_files[self.level], (st.screen_width, st.screen_height))
        self.screen.blit(self.back_image, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render(st.level_text[self.level], True, 'red')
        text_rect = text.get_rect()
        text_rect.center = (st.screen_width * 0.5, st.screen_height * 0.5)
        mouse = pygame.mouse.get_pos()
        if not text_rect.collidepoint(mouse):
            self.screen.blit(text, text_rect)
            pygame.display.update()
        if text_rect.collidepoint(mouse):
            self.write_text(st.level_text[self.level], 60, (st.screen_width * 0.5, st.screen_height * 0.5), 'green')
            pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pygame.mixer.music.load(st.start_level_sound)
                pygame.mixer.music.play()
                pygame.time.wait(500)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(st.back_music[self.level]), - 1)
                self.init_level()
                self.play = True

    def level_loop(self):
        """Performs and checks the required in active game"""
        self.enemy_shoot()
        self.draw_objects()
        self.show_display()
        self.keys_handler()
        self.move_objects()
        self.check_collisions()
        self.check_win()
        pygame.display.update()

    def draw_objects(self):
        """His name tells about him"""
        self.screen.blit(self.back_image, (0, 0))
        self.screen.blit(self.player_image, self.player.rect.topleft)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.enemy.draw(self.screen)

    def show_display(self):
        """Shows the captions of life and score"""
        self.write_text(f'life : {self.life}', 30, (st.screen_width * 0.05, int(st.screen_height * 0.95)), (235, 204, 52))
        self.write_text(f'score : {self.score}', 30, ((st.screen_width * 0.9), int(st.screen_height * 0.95)), (235, 204, 52))
        if self.bullet_saver:
            self.write_text(f'bullets : {self.bullet_counter}', 30, ((st.screen_width * 0.5), int(st.screen_height * 0.95)),(235, 204, 52))
        else:
            self.write_text(f'bullets : {self.bullet_counter}', 30, ((st.screen_width * 0.5), int(st.screen_height * 0.95)),'red')

    def keys_handler(self):
        """Handles with player's move and shooting by keys"""
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.player.move('right', self.player_speed, self.screen_rect)
        elif key[pygame.K_LEFT]:
            self.player.move('left', self.player_speed, self.screen_rect)
        if key[pygame.K_SPACE]:
            shoot = True
            for bullet in self.player_bullets:
                if bullet.rect.bottom > st.screen_height * st.player_shooting_limit[self.level]:
                    shoot = False
                    break
            if shoot:
                self.player_bullets.add(self.player.shoot(self.player_bullet_image))
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(st.player_shooting_sound))
                pygame.mixer.Channel(2).set_volume(0.1)
                self.bullet_counter += 1
                if self.bullet_counter ==  2 * (st.enemy_rows[self.level] * st.enemy_for_row[self.level]):
                    self.bullet_saver = False
                if not self.bullet_saver:
                    self.decrease_score(3)

    def move_objects(self):
        """His name tells about him"""
        self.move_enemy()
        self.move_player_bullets()
        self.move_enemy_bullets()

    def move_enemy(self):
        """Moves regularly right / left / down"""
        if self.flip:
            for enemy in self.enemy:
                enemy.update(pygame.Vector2(0, 12))
            self.flip = False
        else:
            for enemy in self.enemy:
                enemy.update(self.enemy_direction)
            for enemy in self.enemy:
                if enemy.rect.left <= 0 or enemy.rect.right >= st.screen_width:
                    self.enemy_direction *= - 1
                    self.flip = True
                    break

    def move_player_bullets(self):
        """His name tells about him"""
        for bullet in self.player_bullets:
            bullet.update((0, - 1 * st.player_bullet_speed[self.level]), st.screen_height)

    def move_enemy_bullets(self):
        """His name tells about him"""
        for bullet in self.enemy_bullets:
            bullet.update((0, 1 * st.enemy_bullet_speed[self.level]), st.screen_height)

    def enemy_shoot(self):
        """A shooting operation from the enemies at a specified time"""
        time = pygame.time.get_ticks()
        if time % (st.enemy_shooting_rate[self.level] * 60) == 0:
            enemies = random.sample(self.enemy.sprites(), k=min(st.num_enemy_shooting[self.level], len(self.enemy)))
            for enemy in enemies:
                self.enemy_bullets.add(enemy.shoot(self.enemy_bullet_image))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(st.enemy_shooting_sound))

    def check_collisions(self):
        """His name tells about him"""
        # Clash between player shooting and enemies:
        enemies = pygame.sprite.groupcollide(self.enemy, self.player_bullets, True, True)
        for enemy in enemies:
            self.score += enemy.value
        # Clash between enemy shooting and the player:
        bullet = pygame.sprite.spritecollideany(self.player, self.enemy_bullets)
        if bullet:
            bullet.kill()
            self.decrease_life()
            pygame.mixer.Channel(4).play(pygame.mixer.Sound(st.decrease_life_sound))
            self.decrease_score(15)
            self.check_life()
        # A collision between the enemies shooting and the player shooting:
        bullets = pygame.sprite.groupcollide(self.player_bullets, self.enemy_bullets, True, True)
        if bullets:
            pygame.mixer.Channel(3).play(pygame.mixer.Sound(st.bullets_collision_sound))
        # The enemies came down across the border:
        for enemy in self.enemy:
            if enemy.rect.bottom >= self.player.rect.top:
                self.game_over()

    def check_life(self):
        """His name tells about him"""
        if self.life <= 0:
            self.game_over()

    def check_win(self):
        """His name tells about him"""
        if not self.enemy.sprites():
            # Play victory music:
            pygame.mixer.Channel(0).stop()
            pygame.mixer.music.load(st.victory_sound[self.level])
            pygame.mixer.music.play()
            # Show a victory caption and the accumulated score:
            self.screen.blit(self.back_image, (0, 0))
            self.write_text('Great victory ! ! !  ', 60, (st.screen_width * 0.5, st.screen_height * 0.5), 'green')
            self.write_text(f'your score is : {self.score}', 45, (st.screen_width * 0.5, st.screen_height * 0.6), 'green')
            pygame.display.update()
            pygame.time.wait(4000)
            self.level += 1
            self.play = False

    def game_over(self):
        """His name tells about him"""
        # Play loss music:
        pygame.mixer.stop()
        pygame.mixer.music.load(st.game_over_sound)
        pygame.mixer.music.play()
        # Show a loss caption:
        self.screen.blit(self.back_image, (0, 0))
        self.write_text('game over', 80, (st.screen_width * 0.5, st.screen_height * 0.4), 'green')
        self.write_text('try again', 65, (st.screen_width * 0.5, st.screen_height * 0.5), 'green')
        pygame.display.update()
        pygame.time.wait(2500)
        self.level = 1
        self.play = False

    def init_level(self):
        """Initializes settings before each level"""
        if self.level == 1:
            self.score = 0
            self.player = ent.Player(self.player_image, st.player_position)
            self.player_bullets = pygame.sprite.Group()
            self.enemy = pygame.sprite.Group()
            self.enemy_bullets = pygame.sprite.Group()
        else:
            self.player.rect.center = st.player_position
            self.player_bullets.empty()
            self.enemy_bullets.empty()
        self.player_speed = st.player_speed[self.level]
        self.life = 3
        self.enemy_direction = pygame.Vector2(1, 0) * st.enemy_speed[self.level]
        self.flip = None
        self.player.rect.center = st.player_position
        self.create_enemies()
        self.bullet_counter = 0
        self.bullet_saver = True

    def create_enemies(self):
        """His name tells about him"""
        my_range = st.enemy_size[0] * 1.3
        height = my_range
        for row in range(st.enemy_rows[self.level]):
            width = (st.screen_width // 2) - (st.enemy_for_row[self.level] / 2 * my_range)
            for position in range(st.enemy_for_row[self.level]):
                enemy = ent.Enemy(self.enemy_image, st.enemy_life[self.level], \
                                         (width, height), ((st.enemy_rows[self.level] * 10) - (row * 10)))
                self.enemy.add(enemy)
                width += my_range
            height += my_range

    def decrease_life(self):
        """His name tells about him"""
        self.life -= 1

    def decrease_score(self, number):
        """His name tells about him"""
        self.score -= number

    def write_text(self, text, size, position, color):
        """His name tells about him"""
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def create_image(self, file, size):
        """His name tells about him"""
        image = pygame.transform.scale(pygame.image.load(file), size)
        return image
