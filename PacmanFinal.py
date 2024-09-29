import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Variables
WIDTH, HEIGHT = 640, 480  # Screen dimensions
FPS = 60  # Frames per second

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man Game')

# Load and play background music
pygame.mixer.music.load('background_music.mp3')  # Ensure this file exists in the same directory
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Define Pac-Man
pacman_size = 10
pacman_x = WIDTH // 2
pacman_y = HEIGHT // 2
pacman_speed = 4

# Define walls (creating a more complex maze)
walls = [
    pygame.Rect(50, 50, 540, 20),
    pygame.Rect(50, 50, 20, 380),
    pygame.Rect(50, 410, 540, 20),
    pygame.Rect(570, 50, 20, 380),
    pygame.Rect(150, 150, 20, 200),
    pygame.Rect(150, 250, 60, 20),
    pygame.Rect(100, 150, 20, 100),
    pygame.Rect(250, 150, 200, 20),
    pygame.Rect(350, 250, 20, 100),
    pygame.Rect(350, 250, 200, 20),
    pygame.Rect(450, 150, 20, 200),
    pygame.Rect(150, 350, 200, 20),
]

# Define pellets
pellets = [pygame.Rect(x, y, 10, 10) for x in range(70, WIDTH-70, 40) for y in range(70, HEIGHT-70, 40) if not any(w.collidepoint(x, y) for w in walls)]

# Ghosts
ghosts = [
    {'rect': pygame.Rect(100, 100, 20, 20), 'speed': 1}
]

# Score and Lives
score = 0
lives = 3
game_over = False
won = False

# Timer
start_ticks = pygame.time.get_ticks()  # Starting tick
timer_seconds = 90  # 90 seconds

# Game loop control
clock = pygame.time.Clock()

# Define Pac-Man Movement
def move_pacman(keys_pressed, x, y):
    if keys_pressed[pygame.K_LEFT]:
        x -= pacman_speed
    if keys_pressed[pygame.K_RIGHT]:
        x += pacman_speed
    if keys_pressed[pygame.K_UP]:
        y -= pacman_speed
    if keys_pressed[pygame.K_DOWN]:
        y += pacman_speed
    return x, y

# Draw Pac-Man
def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), pacman_size)
    pygame.draw.polygon(screen, BLACK, [(x, y), (x + pacman_size, y - pacman_size // 2), (x + pacman_size, y + pacman_size // 2)])

# Draw Walls
def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)

# Draw Pellets
def draw_pellets():
    for pellet in pellets:
        pygame.draw.rect(screen, WHITE, pellet)

# Draw Ghosts
def draw_ghosts():
    for ghost in ghosts:
        pygame.draw.rect(screen, RED, ghost['rect'])

# Check for collisions
def check_collisions(x, y):
    pacman_rect = pygame.Rect(x - pacman_size, y - pacman_size, pacman_size * 2, pacman_size * 2)
    for wall in walls:
        if pacman_rect.colliderect(wall):
            return True
    return False

# Collect Pellets
def collect_pellets(x, y):
    global score
    pacman_rect = pygame.Rect(x - pacman_size, y - pacman_size, pacman_size * 2, pacman_size * 2)
    for pellet in pellets[:]:
        if pacman_rect.colliderect(pellet):
            pellets.remove(pellet)
            score += 1

# Move Ghosts
def move_ghosts():
    for ghost in ghosts:
        ghost_x, ghost_y = ghost['rect'].center

        # Determine direction towards Pac-Man
        dx = pacman_x - ghost_x
        dy = pacman_y - ghost_y

        if abs(dx) > abs(dy):  # Move horizontally first
            ghost['rect'].x += ghost['speed'] if dx > 0 else -ghost['speed']
        else:  # Move vertically first
            ghost['rect'].y += ghost['speed'] if dy > 0 else -ghost['speed']

# Check Game Over Condition
def check_game_over():
    pacman_rect = pygame.Rect(pacman_x - pacman_size, pacman_y - pacman_size, pacman_size * 2, pacman_size * 2)
    for ghost in ghosts:
        if pacman_rect.colliderect(ghost['rect']):
            return True
    return False

# Display Game Over Message
def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over!', True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Display Win Message
def display_win():
    font = pygame.font.Font(None, 74)
    text = font.render('You Won!', True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Display Lives
def display_lives():
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Lives: {lives}', True, YELLOW)
    screen.blit(lives_text, (80, 30))

# Display Score
def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, YELLOW)
    screen.blit(score_text, (10, 10))

# Display Timer
def display_timer():
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Convert milliseconds to seconds
    remaining_time = max(timer_seconds - elapsed_time, 0)
    timer_text = f'Time: {int(remaining_time)}'
    font = pygame.font.Font(None, 36)
    timer_surface = font.render(timer_text, True, YELLOW)
    screen.blit(timer_surface, (WIDTH - 150, 30))
    return remaining_time <= 0

# Game Loop
while True:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not won:
        # Pac-Man Movement
        keys_pressed = pygame.key.get_pressed()
        new_x, new_y = move_pacman(keys_pressed, pacman_x, pacman_y)

        if not check_collisions(new_x, new_y):
            pacman_x, pacman_y = new_x, new_y

        # Collect pellets
        collect_pellets(pacman_x, pacman_y)

        # Move ghosts
        move_ghosts()

        # Check for game over
        if check_game_over():
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset Pac-Man's position if a life is lost
                pacman_x = WIDTH // 2
                pacman_y = HEIGHT // 2

        # Check for win condition
        if score == 97:
            won = True

        # Check timer
        if display_timer():
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset Pac-Man's position if a life is lost
                pacman_x = WIDTH // 2
                pacman_y = HEIGHT // 2

    # Drawing elements
    draw_walls()
    draw_pellets()
    draw_pacman(pacman_x, pacman_y)
    draw_ghosts()

    # Display lives and score
    display_lives()
    display_score()

    # Display timer
    if not game_over:  # Only show the timer if the game is not over
        display_timer()

    # Display game over message if needed
    if game_over:
        display_game_over()

    # Display win message if needed
    if won:
        display_win()

    # Refresh Screen
    pygame.display.update()

    # Frame Rate Control
    clock.tick(FPS)
