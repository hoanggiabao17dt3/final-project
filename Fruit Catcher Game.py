import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Catcher Game")

# Tải ảnh
background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Điều chỉnh kích thước hình nền
basket_img = pygame.image.load('basket.png')
fruit_img = pygame.image.load('fruit.png')

# Đặt biểu tượng cửa sổ bằng ảnh fruit.png
pygame.display.set_icon(fruit_img)

# Tải âm thanh
catch_sound = pygame.mixer.Sound('vacham.wav')

# Thuộc tính giỏ
basket_width = 100
basket_height = 100
basket_x = SCREEN_WIDTH // 2 - basket_width // 2
basket_y = SCREEN_HEIGHT - basket_height
basket_speed = 10

# Thuộc tính quả
fruit_width = 50
fruit_height = 50
fruit_x = random.randint(0, SCREEN_WIDTH - fruit_width)
fruit_y = -fruit_height
fruit_speed = 5
initial_fruit_speed = fruit_speed

# Điểm số
score = 0
highscore = 0
font = pygame.font.SysFont(None, 55)

def draw_background():
    screen.blit(background_img, (0, 0))

def draw_basket(x, y):
    screen.blit(basket_img, (x, y))

def draw_fruit(x, y):
    screen.blit(fruit_img, (x, y))

def display_score(score, highscore):
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, [10, 10])
    highscore_text = font.render("Highscore: " + str(highscore), True, BLACK)
    screen.blit(highscore_text, [10, 60])

def game_over():
    global score, highscore, fruit_speed
    if score > highscore:
        highscore = score
    screen.fill(WHITE)
    over_text = font.render("Game Over!", True, RED)
    screen.blit(over_text, [SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - over_text.get_height() // 2])
    pygame.display.flip()
    pygame.time.wait(2000)
    score = 0
    fruit_speed = initial_fruit_speed
    reset_game()

def reset_game():
    global fruit_x, fruit_y
    fruit_x = random.randint(0, SCREEN_WIDTH - fruit_width)
    fruit_y = -fruit_height

# Vòng lặp game chính
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
        basket_x += basket_speed

    # Cập nhật vị trí quả
    fruit_y += fruit_speed

    # Kiểm tra va chạm với giỏ
    if basket_y < fruit_y + fruit_height and basket_x < fruit_x + fruit_width and basket_x + basket_width > fruit_x:
        score += 1
        fruit_x = random.randint(0, SCREEN_WIDTH - fruit_width)
        fruit_y = -fruit_height
        catch_sound.play()  # Phát âm thanh khi hứng trúng

        # Tăng tốc độ rơi của quả sau mỗi 2 điểm
        if score % 2 == 0:
            fruit_speed += 1

    # Kiểm tra nếu quả rơi ra khỏi màn hình
    if fruit_y > SCREEN_HEIGHT:
        game_over()

    # Vẽ mọi thứ
    draw_background()
    draw_basket(basket_x, basket_y)
    draw_fruit(fruit_x, fruit_y)
    display_score(score, highscore)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
