import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Hàm tính toán diện tích và chu vi
def calculate():
    shape = shape_var.get()
    try:
        if shape == "Tam giác":
            base = float(entry_base.get())
            height = float(entry_height.get())
            side1 = float(entry_side1.get())
            side2 = float(entry_side2.get())
            side3 = float(entry_side3.get())
            area = 0.5 * base * height
            perimeter = side1 + side2 + side3
            result_text.set(f"Diện tích: {area}\nChu vi: {perimeter}")
            draw_triangle(base, height)

        elif shape == "Hình chữ nhật":
            length = float(entry_length.get())
            width = float(entry_width.get())
            area = length * width
            perimeter = 2 * (length + width)
            result_text.set(f"Diện tích: {area}\nChu vi: {perimeter}")
            draw_rectangle(length, width)

        elif shape == "Hình tròn":
            radius = float(entry_radius.get())
            area = np.pi * (radius ** 2)
            perimeter = 2 * np.pi * radius
            result_text.set(f"Diện tích: {area}\nChu vi: {perimeter}")
            draw_circle(radius)

        elif shape == "Hình thang":
            base1 = float(entry_base1.get())
            base2 = float(entry_base2.get())
            height = float(entry_height_trapezoid.get())
            side1 = float(entry_side1_trapezoid.get())
            side2 = float(entry_side2_trapezoid.get())
            area = 0.5 * (base1 + base2) * height
            perimeter = base1 + base2 + side1 + side2
            result_text.set(f"Diện tích: {area}\nChu vi: {perimeter}")
            draw_trapezoid(base1, base2, height)

        elif shape == "Hình trụ":
            radius = float(entry_cylinder_radius.get())
            height = float(entry_cylinder_height.get())
            volume = np.pi * (radius ** 2) * height
            surface_area = 2 * np.pi * radius * (height + radius)
            result_text.set(f"Thể tích: {volume}\nDiện tích bề mặt: {surface_area}")
            draw_cylinder(radius, height)

        elif shape == "Hình nón":
            radius = float(entry_cone_radius.get())
            height = float(entry_cone_height.get())
            slant_height = float(entry_cone_slant_height.get())
            volume = (1/3) * np.pi * (radius ** 2) * height
            surface_area = np.pi * radius * (radius + slant_height)
            result_text.set(f"Thể tích: {volume}\nDiện tích bề mặt: {surface_area}")
            draw_cone(radius, height, slant_height)

        elif shape == "Cầu":
            radius = float(entry_sphere_radius.get())
            volume = (4/3) * np.pi * (radius ** 3)
            surface_area = 4 * np.pi * (radius ** 2)
            result_text.set(f"Thể tích: {volume}\nDiện tích bề mặt: {surface_area}")
            draw_sphere(radius)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số.")

# Hàm vẽ hình
def draw_triangle(base, height):
    plt.figure()
    plt.fill([0, base, base / 2], [0, 0, height], 'b', alpha=0.5)
    plt.xlim(-1, base + 1)
    plt.ylim(-1, height + 1)
    plt.title("Tam giác")
    plt.xlabel("Chiều rộng")
    plt.ylabel("Chiều cao")
    plt.grid()
    plt.show()

def draw_rectangle(length, width):
    plt.figure()
    plt.fill([0, length, length, 0], [0, 0, width, width], 'g', alpha=0.5)
    plt.xlim(-1, length + 1)
    plt.ylim(-1, width + 1)
    plt.title("Hình chữ nhật")
    plt.xlabel("Chiều dài")
    plt.ylabel("Chiều rộng")
    plt.grid()
    plt.show()

def draw_circle(radius):
    theta = np.linspace(0, 2 * np.pi, 100)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    plt.figure()
    plt.fill(x, y, 'r', alpha=0.5)
    plt.xlim(-radius - 1, radius + 1)
    plt.ylim(-radius - 1, radius + 1)
    plt.title("Hình tròn")
    plt.xlabel("Bán kính")
    plt.ylabel("Bán kính")
    plt.grid()
    plt.gca().set_aspect('equal')
    plt.show()

def draw_trapezoid(base1, base2, height):
    x = [0, base1, base2, 0]
    y = [0, 0, height, height]
    plt.figure()
    plt.fill(x, y, 'y', alpha=0.5)
    plt.xlim(-1, max(base1, base2) + 1)
    plt.ylim(-1, height + 1)
    plt.title("Hình thang")
    plt.xlabel("Chiều dài")
    plt.ylabel("Chiều cao")
    plt.grid()
    plt.show()

def draw_cylinder(radius, height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.linspace(0, height, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.5)
    ax.set_title("Hình trụ")
    plt.show()

def draw_cone(radius, height, slant_height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = np.linspace(0, height, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * (height - z_grid) / height * np.cos(theta_grid)
    y_grid = radius * (height - z_grid) / height * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.5)
    ax.set_title("Hình nón")
    plt.show()

def draw_sphere(radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.5)
    ax.set_title("Cầu")
    plt.show()

# Khởi tạo ứng dụng
app = tk.Tk()
app.title("Ứng Dụng Tính Toán Hình Học")

shape_var = tk.StringVar(value="Tam giác")

# Chọn hình học
tk.Label(app, text="Chọn hình:").pack()
tk.OptionMenu(app, shape_var, "Tam giác", "Hình chữ nhật", "Hình tròn", "Hình thang", "Hình trụ", "Hình nón", "Cầu").pack()

# Nhập dữ liệu
entry_base = tk.Entry(app)
entry_height = tk.Entry(app)
entry_side1 = tk.Entry(app)
entry_side2 = tk.Entry(app)
entry_side3 = tk.Entry(app)

entry_length = tk.Entry(app)
entry_width = tk.Entry(app)

entry_radius = tk.Entry(app)

entry_base1 = tk.Entry(app)
entry_base2 = tk.Entry(app)
entry_height_trapezoid = tk.Entry(app)
entry_side1_trapezoid = tk.Entry(app)
entry_side2_trapezoid = tk.Entry(app)

entry_cylinder_radius = tk.Entry(app)
entry_cylinder_height = tk.Entry(app)

entry_cone_radius = tk.Entry(app)
entry_cone_height = tk.Entry(app)
entry_cone_slant_height = tk.Entry(app)

entry_sphere_radius = tk.Entry(app)

def show_entries():
    for widget in app.winfo_children():
        widget.pack_forget()  # Ẩn tất cả widget
    tk.Label(app, text="Chọn hình:").pack()
    tk.OptionMenu(app, shape_var, "Tam giác", "Hình chữ nhật", "Hình tròn", "Hình thang", "Hình trụ", "Hình nón", "Cầu").pack()
    
    if shape_var.get() == "Tam giác":
        entry_base.pack()
        entry_height.pack()
        entry_side1.pack()
        entry_side2.pack()
        entry_side3.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Hình chữ nhật":
        entry_length.pack()
        entry_width.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Hình tròn":
        entry_radius.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Hình thang":
        entry_base1.pack()
        entry_base2.pack()
        entry_height_trapezoid.pack()
        entry_side1_trapezoid.pack()
        entry_side2_trapezoid.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Hình trụ":
        entry_cylinder_radius.pack()
        entry_cylinder_height.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Hình nón":
        entry_cone_radius.pack()
        entry_cone_height.pack()
        entry_cone_slant_height.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()
    elif shape_var.get() == "Cầu":
        entry_sphere_radius.pack()
        tk.Button(app, text="Tính toán", command=calculate).pack()

shape_var.trace("w", lambda *args: show_entries())

result_text = tk.StringVar()
tk.Label(app, textvariable=result_text).pack()

show_entries()  # Hiển thị trường nhập đầu tiên

app.mainloop()