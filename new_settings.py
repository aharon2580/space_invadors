import pygame


class Settings:
    def __init__(self):

        # General Settings:
        self.screen_width, self.screen_height = 1200, 950
        self.back_image_files = [0, 'background1.jpg', 'back2.jpg', 'back3.jpg']
        self.level_text = [0, 'time to play !', 'go to level 2 !', 'go to level 3 !']
        self.back_music = [0, 'BackMus1.mp3', 'BackMus2.mp3', 'BackMus3.mp3']
        self.victory_sound = [0, 'victory1.mp3', 'victory2.mp3', 'victory3.mp3']
        self.start_level_sound = 'start_level.wav'
        self.game_over_sound = 'game_over.wav'

        # Player settings:
        self.player_image = 'ship.bmp'
        self.player_size = (self.screen_width // 15, self.screen_height // 15)
        self.player_speed = [0, 5, 6, 7]
        self.player_position = (self.screen_width // 2, self.screen_height * 0.85)
        self.player_life = 3
        self.decrease_life_sound = 'decrease_life.mp3'
        self.player_shooting_sound = 'ship_shooting.mp3'
        self.player_shooting_limit = [0, 0.65, 0.68, 0.7]

        # Enemy settings:
        self.enemy_image = 'alien.bmp'
        self.enemy_size = (self.screen_width // 15, self.screen_height // 15)
        self.enemy_for_row = [0, 6, 6, 8]
        self.enemy_rows = [0, 3, 4, 4]
        self.enemy_speed = [0, 2, 4, 6]
        self.enemy_life = [0, 1, 1, 2]
        self.enemy_shooting_rate = [0, 2, 1.5, 1]
        self.num_enemy_shooting = [0, 1, 1, 2]
        self.enemy_shooting_sound = 'EnemiesShoot.wav'

        # Shooting settings:
        self.player_bullet_image = 'ship_bullet.png'
        self.player_bullet_size = (self.screen_width // 45, self.screen_height // 35)
        self.player_bullet_speed = [0, 15, 18, 20]
        self.enemy_bullet_image = 'enemy_bullet.png'
        self.enemy_bullet_size = (self.screen_width // 45, self.screen_height // 35)
        self.enemy_bullet_speed = [0, 15, 18, 20]
        self.bullets_collision_sound = 'bullets_collision.mp3'
