import pgzrun
import random
import math
from pygame import Rect
import pygame
import os

# Game constants
WIDTH = 1000
HEIGHT = 600
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2
WORLD_WIDTH = 2000  # Largura do mundo
CAMERA_X = 0  # Posição da câmera

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3

# Current game state
game_state = MENU
music_enabled = True
sounds_enabled = True
score = 0
level = 1

# Game objects
hero = None
enemies = []
platforms = []
obstacles = []
coins = []

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        self.is_jumping = False
        self.is_running = False
        
    def update(self):
        # Handle input
        keys = keyboard
        
        # Horizontal movement
        self.vel_x = 0
        if keys.left:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
            self.is_running = True
        elif keys.right:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
            self.is_running = True
        else:
            self.is_running = False
        
        # Jumping
        if keys.space and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            self.is_jumping = True
            if sounds_enabled:
                play_jump_sound()
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Keep player in world bounds
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - self.width:
            self.x = WORLD_WIDTH - self.width
        
        # Check ground collision
        if self.y >= HEIGHT - 100:  # Ground level
            self.y = HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False
        
        # Check platform collisions
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                # Landing on top of platform
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                # Hitting platform from below
                elif self.vel_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                # Hitting platform from the side
                elif self.vel_x > 0 and self.x < platform.x:
                    self.x = platform.x - self.width
                elif self.vel_x < 0 and self.x > platform.x:
                    self.x = platform.x + platform.width
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def draw(self):
        # Calculate screen position (relative to camera)
        screen_x = self.x - CAMERA_X
        screen_y = self.y
        
        # Only draw if on screen
        if screen_x > -self.width and screen_x < WIDTH:
            # Draw hero as animated character
            color = (0, 150, 255)  # Blue
            
            # Animation effects
            if self.is_jumping:
                color = (0, 200, 255)  # Lighter blue when jumping
            elif self.is_running:
                color = (0, 100, 255)  # Darker blue when running
            
            # Body
            body_rect = Rect(screen_x + 8, screen_y + 8, self.width - 16, self.height - 16)
            screen.draw.filled_rect(body_rect, color)
        
            # Head
            head_size = 12
            head_x = screen_x + (self.width - head_size) // 2
            head_y = screen_y + 4
            head_rect = Rect(head_x, head_y, head_size, head_size)
            screen.draw.filled_rect(head_rect, (255, 200, 150))  # Skin color
            
            # Eyes
            eye_size = 2
            if self.facing_right:
                eye_x = head_x + 8
            else:
                eye_x = head_x + 2
            eye_y = head_y + 3
            screen.draw.filled_rect(Rect(eye_x, eye_y, eye_size, eye_size), (0, 0, 0))
            
            # Legs (animation)
            leg_width = 4
            leg_height = 8
            leg_y = screen_y + self.height - leg_height
            
            if self.is_running:
                # Animated legs
                offset = math.sin(self.animation_frame * 0.5) * 2
                left_leg_x = screen_x + 6 + offset
                right_leg_x = screen_x + self.width - 10 - offset
            else:
                left_leg_x = screen_x + 6
                right_leg_x = screen_x + self.width - 10
            
            screen.draw.filled_rect(Rect(left_leg_x, leg_y, leg_width, leg_height), color)
            screen.draw.filled_rect(Rect(right_leg_x, leg_y, leg_width, leg_height), color)
            
            # Health bar
            if self.health < self.max_health:
                bar_width = (self.health / self.max_health) * self.width
                health_rect = Rect(screen_x, screen_y - 8, bar_width, 4)
                screen.draw.filled_rect(health_rect, (255, 0, 0))

class Enemy:
    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.vel_x = -ENEMY_SPEED
        self.vel_y = 0
        self.type = enemy_type
        self.health = 30 if enemy_type == "basic" else 50
        self.max_health = self.health
        self.animation_frame = 0
        self.animation_timer = 0
        self.on_ground = False
        self.patrol_start = x - 50  # Área de patrulha
        self.patrol_end = x + 50
        self.is_attacking = False
        self.attack_timer = 0
        
    def update(self, hero):
        # Check if hero is nearby (within attack range)
        distance_to_hero = abs(self.x - hero.x)
        if distance_to_hero < 100:  # Attack range
            self.is_attacking = True
            self.attack_timer = 60  # Attack for 1 second
        else:
            self.is_attacking = False
        
        if self.is_attacking and self.attack_timer > 0:
            # Move towards hero
            if hero.x < self.x:
                self.vel_x = -ENEMY_SPEED * 1.5  # Faster when attacking
            else:
                self.vel_x = ENEMY_SPEED * 1.5
            self.attack_timer -= 1
        else:
            # Normal patrol behavior
            # Reverse direction at patrol boundaries
            if self.x <= self.patrol_start or self.x >= self.patrol_end:
                self.vel_x = -self.vel_x
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check ground collision
        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.vel_y = 0
            self.on_ground = True
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= 12:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3
    
    def draw(self):
        # Calculate screen position (relative to camera)
        screen_x = self.x - CAMERA_X
        screen_y = self.y
        
        # Only draw if on screen
        if screen_x > -self.width and screen_x < WIDTH:
            # Draw enemy
            if self.is_attacking:
                if self.type == "basic":
                    color = (255, 50, 50)  # Darker red when attacking
                else:
                    color = (255, 100, 0)  # Darker orange when attacking
            else:
                if self.type == "basic":
                    color = (255, 100, 100)  # Red
                else:
                    color = (255, 150, 0)  # Orange
            
            # Animation effect
            size_offset = math.sin(self.animation_frame * 0.3) * 2
            
            # Body
            body_rect = Rect(screen_x + 4, screen_y + 4, 
                            self.width - 8 + size_offset, self.height - 8 + size_offset)
            screen.draw.filled_rect(body_rect, color)
            
            # Eyes
            eye_size = 3
            left_eye = Rect(screen_x + 6, screen_y + 6, eye_size, eye_size)
            right_eye = Rect(screen_x + self.width - 9, screen_y + 6, eye_size, eye_size)
            screen.draw.filled_rect(left_eye, (255, 255, 255))
            screen.draw.filled_rect(right_eye, (255, 255, 255))
            
            # Pupils
            pupil_size = 1
            screen.draw.filled_rect(Rect(screen_x + 7, screen_y + 7, pupil_size, pupil_size), (0, 0, 0))
            screen.draw.filled_rect(Rect(screen_x + self.width - 8, screen_y + 7, pupil_size, pupil_size), (0, 0, 0))

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        # Calculate screen position (relative to camera)
        screen_x = self.x - CAMERA_X
        screen_y = self.y
        
        # Only draw if on screen
        if screen_x > -self.width and screen_x < WIDTH:
            # Draw platform
            platform_rect = Rect(screen_x, screen_y, self.width, self.height)
            screen.draw.filled_rect(platform_rect, (100, 200, 100))  # Green
            # Add some texture
            for i in range(0, self.width, 16):
                for j in range(0, self.height, 16):
                    texture_rect = Rect(screen_x + i, screen_y + j, 16, 16)
                    screen.draw.rect(texture_rect, (80, 180, 80))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.animation_frame = 0
        self.animation_timer = 0
        self.collected = False
    
    def update(self):
        if not self.collected:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
    
    def draw(self):
        if not self.collected:
            # Calculate screen position (relative to camera)
            screen_x = self.x - CAMERA_X
            screen_y = self.y
            
            # Only draw if on screen
            if screen_x > -self.width and screen_x < WIDTH:
                # Draw coin with animation
                size = 12 + math.sin(self.animation_frame * 0.5) * 2
                coin_rect = Rect(screen_x + (self.width - size) // 2, 
                               screen_y + (self.height - size) // 2, 
                               size, size)
                screen.draw.filled_rect(coin_rect, (255, 215, 0))  # Gold

def init_game():
    global hero, enemies, platforms, obstacles, coins, score, level
    
    # Clear all objects
    enemies.clear()
    platforms.clear()
    obstacles.clear()
    coins.clear()
    
    # Create hero
    hero = Hero(50, HEIGHT - 150)
    
    # Create platforms
    platforms.append(Platform(200, HEIGHT - 200, 150, 20))
    platforms.append(Platform(400, HEIGHT - 300, 150, 20))
    platforms.append(Platform(600, HEIGHT - 250, 150, 20))
    platforms.append(Platform(800, HEIGHT - 350, 150, 20))
    platforms.append(Platform(1000, HEIGHT - 200, 150, 20))
    platforms.append(Platform(1200, HEIGHT - 300, 150, 20))
    platforms.append(Platform(1400, HEIGHT - 250, 150, 20))
    platforms.append(Platform(1600, HEIGHT - 350, 150, 20))
    
    # Create enemies
    enemies.append(Enemy(300, HEIGHT - 124, "basic"))
    enemies.append(Enemy(500, HEIGHT - 124, "basic"))
    enemies.append(Enemy(700, HEIGHT - 124, "strong"))
    enemies.append(Enemy(900, HEIGHT - 124, "basic"))
    enemies.append(Enemy(1100, HEIGHT - 124, "basic"))
    enemies.append(Enemy(1300, HEIGHT - 124, "strong"))
    enemies.append(Enemy(1500, HEIGHT - 124, "basic"))
    enemies.append(Enemy(1700, HEIGHT - 124, "basic"))
    
    # Create coins
    coins.append(Coin(250, HEIGHT - 220))
    coins.append(Coin(450, HEIGHT - 320))
    coins.append(Coin(650, HEIGHT - 270))
    coins.append(Coin(850, HEIGHT - 370))
    coins.append(Coin(1050, HEIGHT - 220))
    coins.append(Coin(1250, HEIGHT - 320))
    coins.append(Coin(1450, HEIGHT - 270))
    coins.append(Coin(1650, HEIGHT - 370))
    
    score = 0
    level = 1

# Inicializar pygame.mixer para sons
pygame.mixer.init()

# Carregar sons
sound_folder = os.path.join(os.getcwd(), 'sounds')

jump_path = os.path.join(sound_folder, 'jump.wav')
coin_path = os.path.join(sound_folder, 'coin.wav')
hit_path = os.path.join(sound_folder, 'hit.wav')
victory_path = os.path.join(sound_folder, 'victory.wav')
background_music_path = os.path.join(sound_folder, 'background.wav')

print(f"[DEBUG] Caminho jump.wav: {jump_path}")
print(f"[DEBUG] Caminho coin.wav: {coin_path}")
print(f"[DEBUG] Caminho hit.wav: {hit_path}")
print(f"[DEBUG] Caminho victory.wav: {victory_path}")
print(f"[DEBUG] Caminho background.wav: {background_music_path}")

jump_sound = pygame.mixer.Sound(jump_path)
coin_sound = pygame.mixer.Sound(coin_path)
hit_sound = pygame.mixer.Sound(hit_path)
victory_sound = pygame.mixer.Sound(victory_path)

def play_jump_sound():
    """Play jump sound effect"""
    try:
        jump_sound.play()
    except Exception as e:
        print(f"Erro ao tocar jump.wav: {e}")

def play_coin_sound():
    """Play coin collection sound"""
    try:
        coin_sound.play()
    except Exception as e:
        print(f"Erro ao tocar coin.wav: {e}")

def play_hit_sound():
    """Play hit sound"""
    try:
        hit_sound.play()
    except Exception as e:
        print(f"Erro ao tocar hit.wav: {e}")

def play_background_music():
    """Play background music"""
    try:
        pygame.mixer.music.load(background_music_path)
        pygame.mixer.music.play(-1)  # Loop infinito
    except Exception as e:
        print(f"Erro ao tocar background.wav: {e}")

def stop_background_music():
    """Stop background music"""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Erro ao parar música: {e}")

def draw_menu():
    screen.fill((50, 50, 100))
    
    # Title
    screen.draw.text("PLATFORMER ADVENTURE", 
                    centerx=WIDTH//2, top=100, 
                    fontsize=48, color=(255, 255, 255))
    
    # Buttons
    button_y = 250
    button_height = 50
    button_width = 200
    
    # Start button
    start_rect = Rect(WIDTH//2 - button_width//2, button_y, button_width, button_height)
    screen.draw.filled_rect(start_rect, (0, 150, 0))
    screen.draw.text("COMEÇAR JOGO", 
                    centerx=WIDTH//2, centery=button_y + button_height//2, 
                    fontsize=24, color=(255, 255, 255))
    
    # Music button
    music_rect = Rect(WIDTH//2 - button_width//2, button_y + 70, button_width, button_height)
    music_color = (0, 150, 0) if music_enabled else (150, 0, 0)
    screen.draw.filled_rect(music_rect, music_color)
    music_text = "MÚSICA: LIGADA" if music_enabled else "MÚSICA: DESLIGADA"
    screen.draw.text(music_text, 
                    centerx=WIDTH//2, centery=button_y + 70 + button_height//2, 
                    fontsize=20, color=(255, 255, 255))
    
    # Sounds button
    sounds_rect = Rect(WIDTH//2 - button_width//2, button_y + 140, button_width, button_height)
    sounds_color = (0, 150, 0) if sounds_enabled else (150, 0, 0)
    screen.draw.filled_rect(sounds_rect, sounds_color)
    sounds_text = "SOM: LIGADO" if sounds_enabled else "SOM: DESLIGADO"
    screen.draw.text(sounds_text, 
                    centerx=WIDTH//2, centery=button_y + 140 + button_height//2, 
                    fontsize=20, color=(255, 255, 255))
    
    # Exit button
    exit_rect = Rect(WIDTH//2 - button_width//2, button_y + 210, button_width, button_height)
    screen.draw.filled_rect(exit_rect, (150, 0, 0))
    screen.draw.text("SAIR", 
                    centerx=WIDTH//2, centery=button_y + 210 + button_height//2, 
                    fontsize=24, color=(255, 255, 255))

def draw_game():
    # Draw background
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw ground (extend across world)
    ground_rect = Rect(-CAMERA_X, HEIGHT - 100, WORLD_WIDTH, 100)
    screen.draw.filled_rect(ground_rect, (34, 139, 34))  # Forest green
    
    # Draw platforms
    for platform in platforms:
        platform.draw()
    
    # Draw coins
    for coin in coins:
        coin.draw()
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw()
    
    # Draw hero
    if hero:
        hero.draw()
    
    # Draw UI
    screen.draw.text(f"Vida: {hero.health}/{hero.max_health}", 
                    (10, 10), fontsize=24, color=(255, 255, 255))
    screen.draw.text(f"Pontos: {score}", 
                    (10, 40), fontsize=24, color=(255, 255, 255))
    screen.draw.text(f"Nível: {level}", 
                    (10, 70), fontsize=24, color=(255, 255, 255))
    screen.draw.text(f"No chão: {hero.on_ground}", 
                    (10, 100), fontsize=16, color=(255, 255, 255))
    screen.draw.text(f"Pulando: {hero.is_jumping}", 
                    (10, 120), fontsize=16, color=(255, 255, 255))
    screen.draw.text("Setas para mover, ESPAÇO para pular", 
                    (10, HEIGHT - 30), fontsize=16, color=(255, 255, 255))
    screen.draw.text("ESC para menu", 
                    (WIDTH - 150, HEIGHT - 30), fontsize=16, color=(255, 255, 255))

def update():
    global game_state, score, CAMERA_X
    
    if game_state == PLAYING and hero:
        # Update game objects
        hero.update()
        for enemy in enemies:
            enemy.update(hero)
        for coin in coins:
            coin.update()
        
        # Update camera to follow hero
        CAMERA_X = hero.x - WIDTH // 2
        if CAMERA_X < 0:
            CAMERA_X = 0
        elif CAMERA_X > WORLD_WIDTH - WIDTH:
            CAMERA_X = WORLD_WIDTH - WIDTH
        
        # Check coin collection
        for coin in coins:
            if not coin.collected:
                if (hero.x < coin.x + coin.width and
                    hero.x + hero.width > coin.x and
                    hero.y < coin.y + coin.height and
                    hero.y + hero.height > coin.y):
                    coin.collected = True
                    score += 10
                    if sounds_enabled:
                        play_coin_sound()
        
        # Check enemy collisions
        for enemy in enemies:
            if (hero.x < enemy.x + enemy.width and
                hero.x + hero.width > enemy.x and
                hero.y < enemy.y + enemy.height and
                hero.y + hero.height > enemy.y):
                hero.health -= 20
                if sounds_enabled:
                    play_hit_sound()
                if hero.health <= 0:
                    game_state = GAME_OVER
        
        # Check victory condition
        if hero.x >= WORLD_WIDTH - 50:
            game_state = VICTORY

def draw():
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == GAME_OVER:
        screen.fill((100, 0, 0))
        screen.draw.text("GAME OVER", 
                        centerx=WIDTH//2, centery=HEIGHT//2, 
                        fontsize=48, color=(255, 255, 255))
        screen.draw.text(f"Pontuação Final: {score}", 
                        centerx=WIDTH//2, centery=HEIGHT//2 + 60, 
                        fontsize=24, color=(255, 255, 255))
        screen.draw.text("Pressione R para reiniciar", 
                        centerx=WIDTH//2, centery=HEIGHT//2 + 100, 
                        fontsize=24, color=(255, 255, 255))
    elif game_state == VICTORY:
        screen.fill((0, 100, 0))
        screen.draw.text("VITÓRIA!", 
                        centerx=WIDTH//2, centery=HEIGHT//2, 
                        fontsize=48, color=(255, 255, 255))
        screen.draw.text(f"Pontuação: {score}", 
                        centerx=WIDTH//2, centery=HEIGHT//2 + 60, 
                        fontsize=24, color=(255, 255, 255))
        screen.draw.text("Pressione R para próximo nível", 
                        centerx=WIDTH//2, centery=HEIGHT//2 + 100, 
                        fontsize=24, color=(255, 255, 255))

def on_key_down(key):
    global game_state, music_enabled, sounds_enabled
    
    if game_state == MENU:
        if key == keys.ESCAPE:
            exit()
    elif game_state == PLAYING:
        if key == keys.ESCAPE:
            game_state = MENU
    elif game_state == GAME_OVER or game_state == VICTORY:
        if key == keys.R:
            init_game()
            game_state = PLAYING

def on_mouse_down(pos):
    global game_state, music_enabled, sounds_enabled
    
    if game_state == MENU:
        x, y = pos
        
        # Check button clicks
        button_y = 250
        button_height = 50
        button_width = 200
        button_x = WIDTH//2 - button_width//2
        
        # Start button
        if (button_x <= x <= button_x + button_width and 
            button_y <= y <= button_y + button_height):
            init_game()
            game_state = PLAYING
            if music_enabled:
                play_background_music()
        
        # Music button
        elif (button_x <= x <= button_x + button_width and 
              button_y + 70 <= y <= button_y + 70 + button_height):
            music_enabled = not music_enabled
            if music_enabled:
                play_background_music()
            else:
                stop_background_music()
        
        # Sounds button
        elif (button_x <= x <= button_x + button_width and 
              button_y + 140 <= y <= button_y + 140 + button_height):
            sounds_enabled = not sounds_enabled
        
        # Exit button
        elif (button_x <= x <= button_x + button_width and 
              button_y + 210 <= y <= button_y + 210 + button_height):
            exit()

# Initialize game
pgzrun.go()
