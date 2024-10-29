import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk, Button, StringVar, OptionMenu, messagebox, Scale, HORIZONTAL

# Biến toàn cục để lưu ảnh gốc, ảnh đã thay đổi và ảnh trước đó
original_img = None
resized_img = None
previous_img = None

# Thêm biến kernel_strength để lưu mức độ làm rõ
kernel_strength = 1  # Giá trị mặc định cho mức độ

def adjust_kernel_strength(value):
    global kernel_strength
    kernel_strength = int(value)
    edge_enhance_image()  # Gọi lại hàm xử lý ảnh với kernel mới

def load_image():
    global original_img, resized_img
    filepath = filedialog.askopenfilename()
    if filepath:
        original_img = cv2.imread(filepath, cv2.IMREAD_COLOR)  # Đọc ảnh màu
        print("Image loaded successfully. Processing...")
        process_image(original_img)

def process_image(img):
    global resized_img
    size_option = size_var.get()

    if size_option == "Half":
        resized_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    elif size_option == "Bigger":
        resized_img = cv2.resize(img, (1050, 1610))
    elif size_option == "Stretch Nearest":
        resized_img = cv2.resize(img, (780, 540), interpolation=cv2.INTER_LINEAR)
    elif size_option == "Cubic":
        resized_img = cv2.resize(img, (780, 540), interpolation=cv2.INTER_CUBIC)
    else:  # INTER_AREA
        resized_img = cv2.resize(img, (780, 540), interpolation=cv2.INTER_AREA)

    show_images()

def show_images():
    if original_img is not None and resized_img is not None:
        plt.clf()  # Xóa hình ảnh cũ

        # Hiển thị ảnh gốc
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
        plt.title("Original Image")
        plt.axis('off')

        # Hiển thị ảnh đã chỉnh sửa
        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB) if len(resized_img.shape) == 3 else resized_img, cmap='gray')
        plt.title("Processed Image")
        plt.axis('off')

        plt.pause(0.001)  # Cập nhật hình ảnh

def save_image():
    global resized_img
    if resized_img is None:
        messagebox.showwarning("Cảnh báo", "Không có ảnh đã chỉnh sửa để lưu.")
        return

    # Hộp thoại chọn đường dẫn lưu ảnh
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                              filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if filepath:
        cv2.imwrite(filepath, resized_img)
        print(f"Resized image saved as: {filepath}")

def flip_image(direction):
    global resized_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        if direction == "Horizontal":
            resized_img = cv2.flip(resized_img, 1)  # Lật theo chiều ngang
        elif direction == "Vertical":
            resized_img = cv2.flip(resized_img, 0)  # Lật theo chiều dọc
        show_images()
    else:
        messagebox.showwarning("Cảnh Báo", "Vui lòng tải ảnh trước.")

def rotate_image(angle):
    global resized_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        if angle == 90:
            resized_img = cv2.rotate(resized_img, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            resized_img = cv2.rotate(resized_img, cv2.ROTATE_180)
        elif angle == 270:
            resized_img = cv2.rotate(resized_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        show_images()
    else:
        messagebox.showwarning("Cảnh Báo", "Vui lòng tải ảnh trước.")

def clear_image():
    global original_img, resized_img
    original_img = None
    resized_img = None
    plt.clf()  # Xóa hình ảnh trong giao diện
    plt.title("No Image Loaded")
    plt.axis('off')
    plt.show()
    print("Image cleared.")

def adjust_brightness(value):
    global resized_img, original_img, previous_img
    if original_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        value = int(value) - 100  # Chuyển đổi từ 0-200 thành -100 đến 100
        adjusted = cv2.convertScaleAbs(original_img, alpha=1, beta=value)
        resized_img = adjusted
        show_images()
    else:
        messagebox.showwarning("Cảnh Báo", "Vui lòng tải ảnh trước.")

def adjust_contrast(value):
    global resized_img, original_img, previous_img
    if original_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        value = int(value) / 100  # Chuyển đổi từ 0-200 thành 0 đến 2
        adjusted = cv2.convertScaleAbs(original_img, alpha=value, beta=0)
        resized_img = adjusted
        show_images()
    else:
        messagebox.showwarning("Cảnh Báo", "Vui lòng tải ảnh trước.")

def sharpen_image():
    global resized_img, previous_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        resized_img = cv2.filter2D(resized_img, -1, kernel)
        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to sharpen.")

def excessive_sharpen_image():
    global resized_img, previous_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        kernel = np.array([[0, -1, 0],
                           [-1, 9, -1],
                           [0, -1, 0]])
        resized_img = cv2.filter2D(resized_img, -1, kernel)
        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to excessively sharpen.")

def edge_enhance_image():
    global resized_img, previous_img, kernel_strength, original_img
    if resized_img is not None and original_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        
        # Kernel tùy chỉnh với mức độ do người dùng đặt qua thanh trượt
        kernel = np.array([[0, -1, 0],
                           [-1, kernel_strength, -1],
                           [0, -1, 0]])

        # Áp dụng kernel để làm rõ
        resized_img = cv2.filter2D(original_img, -1, kernel)
        
        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to enhance edges.")

def blur_image():
    global resized_img, previous_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        resized_img = cv2.GaussianBlur(resized_img, (15, 15), 0)
        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to blur.")

def convert_to_bw():
    global resized_img, previous_img
    if resized_img is not None:
        previous_img = resized_img.copy()  # Lưu ảnh trước
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to convert to black and white.")

def remove_background():
    global resized_img
    if resized_img is not None:
        # Sử dụng GrabCut để xóa phông và giữ lại người
        mask = np.zeros(resized_img.shape[:2], np.uint8)

        # Khởi tạo các mảng background và foreground
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Tạo một hình chữ nhật bao quanh đối tượng chính (người)
        height, width = resized_img.shape[:2]
        rect = (10, 10, width - 10, height - 10)

        # Áp dụng GrabCut
        cv2.grabCut(resized_img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # Tạo mặt nạ cuối cùng để giữ lại phần đối tượng chính
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Áp dụng mặt nạ lên ảnh gốc để xóa phông
        img_foreground = resized_img * mask2[:, :, np.newaxis]

        # Cập nhật ảnh đã xử lý
        resized_img = img_foreground

        show_images()
    else:
        messagebox.showwarning("Warning", "No image loaded to remove background.")

def undo_changes():
    global resized_img, previous_img
    if previous_img is not None:
        resized_img = previous_img.copy()
        show_images()
    else:
        messagebox.showwarning("Warning", "No previous image to undo.")

# Tạo giao diện người dùng
root = Tk()
root.title("Ứng dụng xử lý ảnh")

size_var = StringVar(root)
size_var.set("Half")  # Giá trị mặc định

size_options = ["Half", "Bigger", "Stretch Nearest", "Cubic", "Area"]
size_menu = OptionMenu(root, size_var, *size_options)
size_menu.pack(pady=10)

load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(pady=5)

save_button = Button(root, text="Save Resized Image", command=save_image)
save_button.pack(pady=5)

undo_button = Button(root, text="Undo", command=undo_changes)
undo_button.pack(pady=5)

# Nút lật ảnh
flip_horizontal_button = Button(root, text="Flip Horizontal", command=lambda: flip_image("Horizontal"))
flip_horizontal_button.pack(pady=5)
flip_vertical_button = Button(root, text="Flip Vertical", command=lambda: flip_image("Vertical"))
flip_vertical_button.pack(pady=5)

# Nút xoay ảnh
rotate_90_button = Button(root, text="Rotate 90°", command=lambda: rotate_image(90))
rotate_90_button.pack(pady=5)

rotate_180_button = Button(root, text="Rotate 180°", command=lambda: rotate_image(180))
rotate_180_button.pack(pady=5)

rotate_270_button = Button(root, text="Rotate 270°", command=lambda: rotate_image(270))
rotate_270_button.pack(pady=5)

# Nút xóa ảnh
clear_button = Button(root, text="Clear Image", command=clear_image)
clear_button.pack(pady=5)

# Nút làm sắc nét ảnh
sharpen_button = Button(root, text="Sharpen Image", command=sharpen_image)
sharpen_button.pack(pady=5)

# Nút làm sắc nét quá mức
excessive_sharpen_button = Button(root, text="Excessive Sharpening", command=excessive_sharpen_image)
excessive_sharpen_button.pack(pady=5)

# Nút tăng cường cạnh
edge_enhance_button = Button(root, text="Edge Enhancement", command=edge_enhance_image)
edge_enhance_button.pack(pady=5)
kernel_slider = Scale(root, from_= 0, to=15, orient=HORIZONTAL, label="Kernel Strength", command=adjust_kernel_strength)
kernel_slider.pack(pady=10)

# Nút làm mờ ảnh
blur_button = Button(root, text="Blur Image", command=blur_image)
blur_button.pack(pady=5)

# Nút chuyển đổi ảnh sang đen trắng
bw_button = Button(root, text="Convert to Black & White", command=convert_to_bw)
bw_button.pack(pady=5)

# Nút xóa phông
remove_bg_button = Button(root, text="Remove Background", command=remove_background)
remove_bg_button.pack(pady=5)

plt.ion()  # Chế độ tương tác cho matplotlib
plt.show()  # Hiển thị cửa sổ matplotlib

root.mainloop()