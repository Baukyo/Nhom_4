import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import platform

# Hàm mở ảnh từ file
def open_image():
    filepath = filedialog.askopenfilename()
    if filepath:
        create_image_window(filepath)

# Hàm mở camera và chụp ảnh
def capture_and_save_image():
    cap = cv2.VideoCapture(0)  # Mở camera
    if not cap.isOpened():
        print("Không thể mở camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể lấy hình ảnh từ camera.")
            break

        # Hiển thị khung hình từ camera
        cv2.imshow('Camera', frame)

        # Nhấn phím 'c' để chụp ảnh
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    # Đóng camera
    cap.release()
    cv2.destroyAllWindows()

    # Hộp thoại để chọn nơi lưu ảnh
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính Tkinter
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if filepath:
        # Lưu ảnh vào đường dẫn được chọn
        cv2.imwrite(filepath, frame)
        print(f"Ảnh đã được lưu tại: {filepath}")
        create_image_window(filepath)
    else:
        print("Không lưu ảnh.")

# Tạo cửa sổ mới để hiển thị ảnh
def create_image_window(filepath):
    image = cv2.imread(filepath)
    image_window = Toplevel(root)
    image_window.title(filepath)
    image_window.geometry("800x600")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(image_pil)

    canvas = Canvas(image_window, width=800, height=500)
    canvas.pack()
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk

    # Thêm nút xử lý ảnh
    btn_frame = Frame(image_window)
    btn_frame.pack(side=BOTTOM, fill=X)

    btn_gray = Button(btn_frame, text="Chuyển xám", command=lambda: to_grayscale(image, image_window))
    btn_gray.pack(side=LEFT, padx=10, pady=10)

    btn_blur = Button(btn_frame, text="Làm mờ", command=lambda: blur_image(image, image_window))
    btn_blur.pack(side=LEFT, padx=10, pady=10)

# Chuyển ảnh sang grayscale
def to_grayscale(original_img, window):
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    display_in_window(gray_img, window)

# Làm mờ ảnh
def blur_image(original_img, window):
    blurred_img = cv2.GaussianBlur(original_img, (15, 15), 0)
    display_in_window(blurred_img, window)

# Hiển thị ảnh lên cửa sổ mới
def display_in_window(image, window):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(image_pil)

    canvas = Canvas(window, width=800, height=500)
    canvas.pack()
    canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk

# Giao diện chính Tkinter
root = Tk()
root.title("Ứng dụng xử lý ảnh")
root.geometry("300x200")

# Khung nút điều khiển
frame = Frame(root)
frame.pack(side=BOTTOM, fill=X)

# Các nút điều khiển
btn_open = Button(frame, text="Mở ảnh", command=open_image)
btn_open.pack(side=LEFT, padx=10, pady=10)
btn_capture = Button(frame, text="Chụp ảnh", command=capture_and_save_image)
btn_capture.pack(side=LEFT, padx=10, pady=10)

# Khởi chạy giao diện
root.mainloop()
