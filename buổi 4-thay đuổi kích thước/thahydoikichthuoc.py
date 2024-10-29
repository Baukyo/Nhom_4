import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Khởi tạo biến lưu hình ảnh
img = None

# Hàm để tải hình ảnh từ máy tính
def load_image():
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        messagebox.showerror("Error", "Không thể đọc file hình ảnh.")
    else:
        messagebox.showinfo("Thông báo", "Hình ảnh đã được tải thành công.")

# Hàm xử lý và hiển thị hình ảnh theo tùy chọn của người dùng
def apply_filter():
    if img is None:
        messagebox.showerror("Error", "Chưa chọn hình ảnh.")
        return
    
    # Lấy lựa chọn từ combobox
    selected_option = filter_combobox.get()
    
    if selected_option == "Original":
        processed_img = img
    elif selected_option == "Half":
        processed_img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)
    elif selected_option == "Bigger":
        processed_img = cv2.resize(img, (1050, 1610))
    elif selected_option == "Interpolation Nearest":
        processed_img = cv2.resize(img, (780, 540), interpolation=cv2.INTER_LINEAR)
    
    # Hiển thị hình ảnh với Matplotlib
    Titles = [selected_option]
    images = [processed_img]

    plt.figure(figsize=(5, 5))
    for i in range(1):
        plt.subplot(1, 1, i + 1)
        plt.title(Titles[i])
        plt.imshow(images[i], cmap='gray')  # Sử dụng 'gray' cho ảnh grayscale
        plt.axis('off')  # Ẩn trục
    plt.tight_layout()
    plt.show()

# Tạo giao diện người dùng bằng Tkinter
root = tk.Tk()
root.title("Chọn Kích Cỡ Ảnh")

# Nút để tải hình ảnh
load_button = tk.Button(root, text="Tải Hình Ảnh", command=load_image)
load_button.pack(pady=10)

# Combobox để chọn loại filter
filter_label = tk.Label(root, text="Chọn kích cỡ:")
filter_label.pack(pady=5)

filters = ["Original", "Half", "Bigger", "Interpolation Nearest"]
filter_combobox = ttk.Combobox(root, values=filters)
filter_combobox.set("Original")
filter_combobox.pack(pady=5)

# Nút để áp dụng filter và hiển thị hình ảnh
apply_button = tk.Button(root, text="Áp Dụng", command=apply_filter)
apply_button.pack(pady=10)

# Chạy ứng dụng Tkinter
root.mainloop()
