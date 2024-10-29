import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Tiêu đề cửa sổ
pygame.display.set_caption("Game Đua Xe Tránh Chướng Ngại Vật")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Tốc độ khung hình
clock = pygame.time.Clock()
fps = 60

# Khởi tạo xe
car_width = 200
car_height = 150
car_x = screen_width // 2 - car_width // 2
car_y = screen_height - car_height - 10

# Tốc độ xe
car_speed = 5

# Khởi tạo chướng ngại vật
obstacle_width = 100
obstacle_height = 100
obstacle_color = red
obstacles = []

# Tạo chướng ngại vật đầu tiên
def create_obstacle():
  obstacle_x = random.randint(0, screen_width - obstacle_width)
  obstacle_y = -obstacle_height
  obstacles.append([obstacle_x, obstacle_y])

create_obstacle()

# Tạo chướng ngại vật liên tục
obstacle_frequency = 1500  # Tạo chướng ngại vật mỗi 1.5 giây
last_obstacle_time = pygame.time.get_ticks()

# Load hình ảnh xe
car_image = pygame.image.load("img.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (car_width, car_height))

# Load hình ảnh chướng ngại vật
obstacle_image = pygame.image.load("img_1.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# Load hình ảnh background
background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Hàm vẽ xe
def draw_car(x, y):
  screen.blit(car_image, (x, y))

# Hàm vẽ chướng ngại vật
def draw_obstacle(x, y):
  screen.blit(obstacle_image, (x, y))

# Hàm xử lý va chạm
def check_collision(car_x, car_y):
  for obstacle in obstacles:
    obstacle_x, obstacle_y = obstacle
    if (
        car_x < obstacle_x + obstacle_width
        and car_x + car_width > obstacle_x
        and car_y < obstacle_y + obstacle_height
        and car_y + car_height > obstacle_y
    ):
      return True
  return False

# Hàm hiển thị màn hình Game Over
def game_over_screen():
  font = pygame.font.Font(None, 72)
  text = font.render("Game Over", True, white)
  text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
  screen.blit(text, text_rect)

  font = pygame.font.Font(None, 48)
  text = font.render("Enter", True, white)
  text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
  screen.blit(text, text_rect)

  pygame.display.update()

# Khởi tạo biến trạng thái trò chơi
game_over = False
running = True

while running:
  # Xử lý sự kiện
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN:
        if game_over:
          # Khởi tạo lại xe và chướng ngại vật khi chơi lại
          car_x = screen_width // 2 - car_width // 2
          car_y = screen_height - car_height - 10
          obstacles.clear()
          create_obstacle()
          last_obstacle_time = pygame.time.get_ticks()
          game_over = False

  # Di chuyển xe
  if not game_over:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
      car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < screen_width - car_width:
      car_x += car_speed

    # Tạo chướng ngại vật mới
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > obstacle_frequency:
      create_obstacle()
      last_obstacle_time = current_time

    # Di chuyển chướng ngại vật
    for obstacle in obstacles:
      obstacle_x, obstacle_y = obstacle
      obstacle_y += 5
      obstacle[1] = obstacle_y

      # Loại bỏ chướng ngại vật ra khỏi màn hình
      if obstacle_y > screen_height:
        obstacles.remove(obstacle)

    if check_collision(car_x, car_y):
      game_over = True
      game_over_screen()  # Gọi hàm hiển thị màn hình game over
    else:
      # Vẽ lên màn hình
      screen.blit(background_image, (0, 0))  # Vẽ background
      draw_car(car_x, car_y)
      for obstacle in obstacles:
        draw_obstacle(obstacle[0], obstacle[1])

      # Cập nhật màn hình
      pygame.display.update()
      clock.tick(fps)

# Thoát khỏi Pygame
pygame.quit()
quit()