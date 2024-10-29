import pygame
import sys
import random
import time

# Khởi tạo Pygame
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
pygame.init()
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Tải hình ảnh và âm thanh
BG = pygame.image.load('bg2.jpg')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
chim_image = pygame.image.load('chim3.png')
chim_image = pygame.transform.scale(chim_image, (40, 30))
gun_image = pygame.image.load('sung.png')  # Hình ảnh súng
gun_image = pygame.transform.scale(gun_image, (60, 30))  # Thay đổi kích thước nếu cần
bullet_image = pygame.image.load('dansung.png')  # Hình ảnh viên đạn
bullet_image = pygame.transform.scale(bullet_image, (10, 10))  # Thay đổi kích thước nếu cần

# Âm thanh nền
pygame.mixer.init()
background_music = pygame.mixer.Sound('Lofi.mp3')  # Đảm bảo có tệp âm thanh
background_music.play(-1)  # Phát âm thanh nền liên tục

FPS = 20
fpsClock = pygame.time.Clock()
diem = 0
time0 = time.time()
speed = 5  # Tốc độ chim
number_of_birds = 5  # Số lượng chim

# Danh sách để lưu trữ vị trí và trạng thái của các chim
birds = []
for _ in range(number_of_birds):
    bird_x = random.randint(0, WINDOWWIDTH - 40)
    bird_y = random.randint(50, 300)
    birds.append([bird_x, bird_y])

# Danh sách để lưu trữ viên đạn
bullets = []

def show_start_screen():
    """Hiển thị màn hình bắt đầu trò chơi."""
    font = pygame.font.SysFont('Arial', 50)
    title_text = font.render('Chao mung den Tro Choi!', True, (255, 255, 255))
    start_text = font.render('Nhan SPACE de bat dau', True, (255, 255, 255))

    while True:
        w.blit(BG, (0, 0))  # Vẽ nền
        w.blit(title_text, (WINDOWWIDTH // 2 - title_text.get_width() // 2, WINDOWHEIGHT // 2 - 100))
        w.blit(start_text, (WINDOWWIDTH // 2 - start_text.get_width() // 2, WINDOWHEIGHT // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Trở về hàm chính để bắt đầu trò chơi

# Gọi hàm để hiển thị màn hình khởi đầu
show_start_screen()

# Vị trí súng
gun_y = WINDOWHEIGHT - 60

# Vòng lặp chính của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # Thay đổi để bắn khi nhấn chuột
            if event.button == 1:  # Chuột trái
                # Bắn viên đạn
                bullets.append([gun_x + 25, gun_y])  # Tạo viên đạn từ vị trí của súng

    # Lấy vị trí chuột
    mouse_x, _ = pygame.mouse.get_pos()  # Lấy vị trí x của chuột
    gun_x = mouse_x - gun_image.get_width() // 2  # Cập nhật vị trí súng

    # Đảm bảo súng không vượt ra ngoài màn hình
    if gun_x < 0:
        gun_x = 0
    elif gun_x > WINDOWWIDTH - gun_image.get_width():
        gun_x = WINDOWWIDTH - gun_image.get_width()

    w.blit(BG, (0, 0))

    # Cập nhật tốc độ dựa trên điểm số
    speed = 5 + (diem // 20)  # Tăng tốc độ cho mỗi 20 điểm

    # Cập nhật vị trí chim
    for bird in birds:
        bird[0] += speed  # Tăng vị trí x
        if bird[0] > WINDOWWIDTH:  # Nếu chim ra ngoài màn hình
            bird[0] = -40  # Reset vị trí chim
            bird[1] = random.randint(50, 300)  # Đặt vị trí y ngẫu nhiên

        # Vẽ chim
        w.blit(chim_image, (bird[0], bird[1]))

    # Danh sách để lưu trữ viên đạn cần xóa
    bullets_to_remove = []

    # Cập nhật và vẽ viên đạn
    for bullet in bullets[:]:  # Lặp qua bản sao danh sách để tránh lỗi
        bullet[1] -= 10  # Di chuyển viên đạn lên trên
        if bullet[1] < 0:  # Nếu viên đạn ra ngoài màn hình
            bullets_to_remove.append(bullet)  # Đánh dấu viên đạn để xóa
        else:
            w.blit(bullet_image, (bullet[0], bullet[1]))  # Vẽ viên đạn

            # Kiểm tra va chạm giữa viên đạn và chim
            for bird in birds:
                if bird[0] < bullet[0] < bird[0] + 40 and bird[1] < bullet[1] < bird[1] + 30:
                    diem += 1  # Tăng điểm
                    bird[0] = -40  # Đưa chim ra ngoài màn hình
                    bullets_to_remove.append(bullet)  # Đánh dấu viên đạn để xóa

    # Xóa viên đạn đã đánh dấu
    for bullet in bullets_to_remove:
        if bullet in bullets:  # Kiểm tra xem viên đạn có trong danh sách hay không
            bullets.remove(bullet)

    # Vẽ súng
    w.blit(gun_image, (gun_x, gun_y))

    time1 = time.time()
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('Tong diem: {} '.format(diem), True, (255, 0, 0))
    text1 = font.render('Thoi gian: {} '.format(int(time1 - time0)), True, (255, 0, 0))
    w.blit(text, (50, 50))
    w.blit(text1, (50, 80))

    pygame.display.update()
    fpsClock.tick(FPS)