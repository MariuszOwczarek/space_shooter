import datetime
import random
import sys
import pygame
import settings
from player import Player
from bullet import Bullet
from alien import Alien
from powerups import Powerups
from hit import HitText


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Space Rage')
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        BG = pygame.image.load('./Graphics/background/bg12.jpeg').convert()
        self.BG_FIT = pygame.transform.scale(BG, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.FONT_small = pygame.font.SysFont('helvetica', 20)
        self.FONT_super_small = pygame.font.SysFont('helvetica', 15)
        self.game_points = 0
        self.game_level = 1
        self.ratio = 1
        self.cost = 0
        self.game_over = False

        # Load and play background music
        pygame.mixer.music.load('./Music/mixkit-space-deploy-whizz-3003.wav')
        pygame.mixer.music.set_volume(0.3)  # Set music volume (30%)
        pygame.mixer.music.play(-1)  # Play the music in an infinite loop

        # Initialize the intro screen
        self.intro_font = pygame.font.SysFont('helvetica', 40)
        self.menu_options = ['Start Game', 'Leaderboard', 'Exit']
        self.selected_option = 0
        self.intro = True

        # Load leaderboard data from a file (if it exists)
        try:
            with open("leaderboard.txt", "r") as file:
                self.leaderboard_data = []
                for line in file:
                    # Split the line into score and date
                    score_str, date_str = line.strip().split(" ")
                    score = int(score_str)
                    date_str = date_str.strip("()")  # Remove the parentheses from the date
                    date = date_str
                    self.leaderboard_data.append((score, date))
        except FileNotFoundError:
            self.leaderboard_data = []


    def intro_screen(self):
        while self.intro:
            self.screen.fill(pygame.Color('black'))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            self.intro = False  # Start the game
                        elif self.selected_option == 1:
                            self.display_leaderboard()  # Display the leaderboard
                        elif self.selected_option == 2:
                            pygame.quit()
                            sys.exit()  # Exit the game

            for i, option in enumerate(self.menu_options):
                color = 'white' if i == self.selected_option else 'gray'
                option_text = self.intro_font.render(option, True, pygame.Color(color))
                self.screen.blit(option_text,
                                (settings.SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                                settings.SCREEN_HEIGHT // 2 + i * 50))

            pygame.display.update()

    def game_over_screen(self):
        self.screen.fill(pygame.Color('black'))
        game_over_font = pygame.font.SysFont('helvetica', 40)

        game_over_text = game_over_font.render("GAME OVER", True, pygame.Color('red'))
        self.screen.blit(game_over_text, (settings.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                        settings.SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        score_text = game_over_font.render(f"Score: {self.game_points}", True, pygame.Color('white'))
        self.screen.blit(score_text, (settings.SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                                    settings.SCREEN_HEIGHT // 2 + score_text.get_height()))

        pygame.display.update()

        # Save the score to the leaderboard
        self.save_to_leaderboard(self.game_points)

        pygame.time.wait(1000)  # Wait for 1 second before showing the confirmation screen


    def display_leaderboard(self):
        leaderboard_font = pygame.font.SysFont('helvetica', 30)

        self.screen.fill(pygame.Color('black'))

        if self.leaderboard_data:
            leaderboard_text = leaderboard_font.render("Leaderboard", True, pygame.Color('white'))
            self.screen.blit(leaderboard_text, (settings.SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, 50))

            y = 100
            for rank, score in enumerate(self.leaderboard_data, start=1):
                score_text = leaderboard_font.render(f"{rank}. {score}", True, pygame.Color('white'))
                self.screen.blit(score_text, (settings.SCREEN_WIDTH // 2 - score_text.get_width() // 2, y))
                y += 40
        else:
            no_data_text = leaderboard_font.render("No scores yet", True, pygame.Color('white'))
            self.screen.blit(no_data_text, (settings.SCREEN_WIDTH // 2 - no_data_text.get_width() // 2,
                                            settings.SCREEN_HEIGHT // 2))

        pygame.display.update()

        # Wait for a few seconds before returning to the intro screen
        pygame.time.wait(3000)

    def save_to_leaderboard(self, score):
        # Add the new score and current date to the leaderboard data and sort it in descending order
        self.leaderboard_data.append((score, datetime.date.today()))
        self.leaderboard_data.sort(reverse=True)

        # Keep only the top 10 scores
        self.leaderboard_data = self.leaderboard_data[:10]

        # Save the updated leaderboard data back to the file with full date
        with open("leaderboard.txt", "w") as file:
            for score, date in self.leaderboard_data:
                file.write(f"{score} ({date})\n")

    def menu_hud(self, player, ratio, bullet_type):
        bar_empty_image = pygame.image.load('./Graphics/other/hp_bar_bg.png').convert_alpha()
        energy_image = pygame.image.load('./Graphics/other/hp_bar.png').convert_alpha()
        energy_image_ratio = energy_image.get_width() * ratio
        energy_text = self.FONT_super_small.render(f'{player.hp}', True, 'White')
        if energy_image_ratio <= 0:
            energy_image = pygame.transform.scale(energy_image, (0, energy_image.get_height()))
        else:
            energy_image = pygame.transform.scale(energy_image, (energy_image_ratio, energy_image.get_height()))

        weapon_image = pygame.image.load(
            f'./Graphics/weapons/{settings.BULLET_DATA[bullet_type]["image"]}.png').convert_alpha()
        # weapon_image = pygame.transform.scale_by(weapon_image_big, 1)

        weapon_qty_text = self.FONT_small.render(f'{settings.BULLET_DATA[bullet_type]["qty"]}', True, 'White')
        level_text = self.FONT_small.render(f'Lvl: {game.game_level}', True, 'White')

        points_text = self.FONT_small.render(f'{game.game_points}', True, 'White')
        additional_bullets_image = pygame.transform.scale_by(
            pygame.image.load('./Graphics/powerups/bullets.png').convert_alpha(), 0.5)
        additional_energy_image = pygame.transform.scale_by(
            pygame.image.load('./Graphics/powerups/energy.png').convert_alpha(), 0.5)

        if self.game_points >= int((5_000 * self.game_level) / 3):
            buy_bullets_text = self.FONT_super_small.render(f'(P)', True, 'White')
            game.screen.blit(buy_bullets_text, (settings.SCREEN_WIDTH - buy_bullets_text.get_width() - 20, 70))
            game.screen.blit(additional_bullets_image, (settings.SCREEN_WIDTH - 60, 68))

        if self.game_points >= int((10_000 * self.game_level) / 3) and player.hp != settings.PLAYER_HP:
            buy_energy_text = self.FONT_super_small.render(f'(O)', True, 'White')
            game.screen.blit(buy_energy_text, (settings.SCREEN_WIDTH - buy_energy_text.get_width() - 20, 90))
            game.screen.blit(additional_energy_image, (settings.SCREEN_WIDTH - 60, 88))

        game.screen.blit(points_text, (settings.SCREEN_WIDTH - points_text.get_width() - 20, 50))
        game.screen.blit(level_text, (settings.SCREEN_WIDTH - level_text.get_width() - 20, 17))
        game.screen.blit(weapon_qty_text, (50, 57))
        game.screen.blit(bar_empty_image, (5, 10))
        game.screen.blit(energy_image, (14, 17))
        game.screen.blit(weapon_image, (8, 50))
        game.screen.blit(energy_text, (68, 19))

        pygame.display.update()

    def buy_powerups(self, player, power_type, cost):
        self.cost = cost
        if power_type == 'bullets' and self.game_points >= self.cost:
            for idx, bullet in enumerate(settings.PLAYER_BULLET_LST):
                settings.BULLET_DATA[bullet]["qty"] += int(settings.POWERUP_DATA[power_type]["bullets"] - idx * 10)

            # Ensure that the quantity does not go below zero
            for bullet in settings.PLAYER_BULLET_LST:
                settings.BULLET_DATA[bullet]["qty"] = max(settings.BULLET_DATA[bullet]["qty"], 0)

            self.game_points -= int(self.cost)

    def run(self):
        player_group = pygame.sprite.Group()
        player_bullet_group = pygame.sprite.Group()
        alien_bullet_group = pygame.sprite.Group()
        alien_group = pygame.sprite.Group()
        powerup_group = pygame.sprite.Group()
        shottext_group = pygame.sprite.Group()

        # noinspection PyTypeChecker
        player = Player(player_group)
        run = True
        select_weapon = 0
        clock = pygame.time.Clock()

        # alien spawn timer
        time_delay_alien = 3000  # 3 seconds
        alien_respawn = pygame.USEREVENT + 0
        pygame.time.set_timer(alien_respawn, time_delay_alien)

        # player bullet timer
        time_delay_bullet = 250  # 0.25 seconds
        bullet_respawn = pygame.USEREVENT + 1
        pygame.time.set_timer(bullet_respawn, time_delay_bullet)

        # Run the intro screen before starting the game
        self.intro_screen()

        while run:
            dt = clock.tick(60) / 1000  # Limit the frame rate to 60 FPS
            weapon_no = settings.PLAYER_BULLET_LST[select_weapon]
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == alien_respawn and len(alien_group) < 10:
                    Alien(pos_x=random.randint(10, settings.SCREEN_WIDTH - 90),
                        pos_y=random.randint(-300, -200),
                        alien_type=random.choice(settings.ALIEN_LST),
                        group=alien_group)

                if event.type == bullet_respawn and keys[pygame.K_SPACE] and \
                        settings.BULLET_DATA[weapon_no]["qty"] > 0:
                    Bullet(pos=player.rect.midtop,
                        direction=-1,
                        bullet_type=weapon_no,
                        resize=0.6,
                        groups=player_bullet_group)
                    settings.BULLET_DATA[weapon_no]["qty"] -= 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.buy_powerups(player, 'bullets', int(5_000 * self.game_level) // 3)
                    if event.key == pygame.K_o:
                        self.buy_powerups(player, 'energy', int(10_000 * self.game_level) // 3)

            # Handle weapon selection based on game_level
            for idx in range(len(settings.PLAYER_BULLET_LST)):
                if keys[pygame.K_1 + idx] and self.game_level >= (idx + 1) * 5:
                    select_weapon = idx

            # Spawning alien bullets based on random value
            for alien in alien_group:
                shoot_check = random.randint(1, 301)
                laser_check = random.choice(settings.ALIEN_BULLET_LST)
                if shoot_check == 1:
                    Bullet(pos=alien.rect.midbottom,
                        direction=1,
                        bullet_type=laser_check,
                        resize=0.5,
                        groups=alien_bullet_group)
                if alien.rect.top > settings.SCREEN_HEIGHT:
                    alien.kill()
                    self.game_points -= 2000

            # Alien bullet and player collision (bullet to player ship)
            for bullet in alien_bullet_group:
                if bullet.rect.colliderect(player.rect):
                    bullet.kill()
                    player.hp -= bullet.damage
                    HitText(entity=player.rect,
                            damage=str(f'{bullet.damage}'),
                            color='white',
                            direction=1,
                            groups=shottext_group)
                    self.ratio = player.hp / settings.PLAYER_HP
                if bullet.rect.y > settings.SCREEN_HEIGHT:
                    bullet.kill()

            # Player bullet and alien collision (bullet to ship)
            modificator = random.randint(-player.modificator, player.modificator)
            for bullet in player_bullet_group:
                for alien in alien_group:
                    if bullet.rect.colliderect(alien.rect):
                        damage_value = (bullet.damage + modificator) - alien.defence
                        if damage_value > 0:
                            alien.defence -= 5
                            alien.hp -= damage_value
                            HitText(entity=alien.rect,
                                    damage=str(f'{damage_value}'),
                                    color='white',
                                    direction=-1,
                                    groups=shottext_group)
                        bullet.kill()
                        if alien.hp <= 0:
                            alien.kill()
                            # If alien killed, choose powerup
                            self.game_points += settings.ALIEN_DATA[alien.alien_type]["points"]
                            lucky_num = random.randint(1, 101)
                            powerup_lst = random.choice(settings.POWERUP_LST)
                            if lucky_num <= settings.POWERUP_DATA[powerup_lst]["chance"]:
                                Powerups(pos_x=random.randint(10, settings.SCREEN_WIDTH - 80),
                                        pos_y=random.randint(-100, -50),
                                        power_type=powerup_lst,
                                        groups=powerup_group)

                if bullet.rect.y < 0:
                    bullet.kill()

            # Player and alien collision (ship to ship)
            for alien in alien_group:
                if alien.rect.colliderect(player.rect):
                    alien.kill()
                    player.kill()
                    player.hp = 0
                    self.ratio = player.hp / settings.PLAYER_HP

            if player.hp <= 0 or game.game_points < 0:
                if not self.game_over:
                    self.game_over_screen()
                    self.game_over = True  # Set game_over flag to True after displaying the game over screen


            # Powerups and player collision (adding items based on power-up)
            for powerup in powerup_group:
                if powerup.rect.colliderect(player.rect):
                    powerup.kill()
                    if powerup.power_type == 'power':
                        self.game_points += settings.POWERUP_DATA[powerup.power_type]["points"]
                    if powerup.power_type == 'energy':
                        player.hp = settings.POWERUP_DATA[powerup.power_type]["hp"]
                        self.ratio = player.hp / settings.PLAYER_HP
                    if powerup.power_type == 'bullets':
                        for idx, bullet in enumerate(settings.PLAYER_BULLET_LST):
                            settings.BULLET_DATA[bullet]["qty"] += int(settings.POWERUP_DATA[powerup.power_type]["bullets"] - idx * 10)
                if powerup.rect.y > settings.SCREEN_HEIGHT:
                    powerup.kill()

            if self.game_over:
                pygame.time.wait(1000)  # Wait for 1 second before returning to the intro screen
                run = False  # Set run to False to exit the game loop
                continue  # Skip the rest of the loop

            # Increase game level if enough points are scored
            if self.game_points != 0 and self.game_points > (2000 * self.game_level) ** 1.06:
                self.game_level += 1
                if time_delay_alien > 1000:
                    time_delay_alien -= 250

            # Update sprite groups and display on screen
            player_bullet_group.update(dt)
            alien_bullet_group.update(dt)
            alien_group.update(dt)
            player_group.update(dt)
            powerup_group.update(dt)
            shottext_group.update(dt)

            self.screen.blit(self.BG_FIT, (0, 0))
            player_group.draw(self.screen)
            player_bullet_group.draw(self.screen)
            alien_bullet_group.draw(self.screen)
            alien_group.draw(self.screen)
            powerup_group.draw(self.screen)
            shottext_group.draw(self.screen)

            # Draw HUD after drawing sprites
            self.menu_hud(player, self.ratio, weapon_no)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()


