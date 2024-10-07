import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def calculate_and_plot():
    result_var.set("")
    integral_var.set("")
    definite_integral_var.set("")
    expression = entry.get()
    x = sp.symbols('x')
    
    try:
        # Tính đạo hàm
        derivative = sp.diff(expression, x)
        result_var.set(f"Đạo hàm: {derivative}")

        # Tính tích phân không xác định
        integral = sp.integrate(expression, x)
        integral_var.set(f"Tích phân không xác định: {integral}")

        # Vẽ đồ thị
        f = sp.lambdify(x, expression, modules=['numpy'])
        f_derivative = sp.lambdify(x, derivative, modules=['numpy'])
        f_integral = sp.lambdify(x, integral, modules=['numpy'])

        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)
        y_derivative_vals = f_derivative(x_vals)
        y_integral_vals = f_integral(x_vals)

        plt.figure(figsize=(10, 5))
        plt.plot(x_vals, y_vals, label=f'Hàm: {expression}', color='blue')
        plt.plot(x_vals, y_derivative_vals, label=f'Đạo hàm: {derivative}', color='red', linestyle='--')
        plt.plot(x_vals, y_integral_vals, label=f'Tích phân: {integral}', color='green', linestyle=':')

        plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
        plt.title('Đồ Thị Hàm Số, Đạo Hàm và Tích Phân')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid()
        plt.show()
    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

def calculate_definite_integral():
    result_var.set("")
    integral_var.set("")
    definite_integral_var.set("")
    expression = entry.get()
    x = sp.symbols('x')

    try:
        # Lấy a và b từ ô nhập
        a = float(lower_limit_entry.get())
        b = float(upper_limit_entry.get())

        # Tính tích phân xác định
        definite_integral = sp.integrate(expression, (x, a, b))
        definite_integral_var.set(f"Tích phân xác định từ {a} đến {b}: {definite_integral}")
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

# Tạo giao diện
app = tk.Tk()
app.title("Ứng Dụng Giải Tích")

# Nhập hàm số
label_expression = tk.Label(app, text="Nhập hàm số (ví dụ: sin(x), x**2)")
label_expression.pack()
entry = tk.Entry(app)
entry.pack()
#entry.insert(0, "Nhập hàm số (ví dụ: sin(x), x**2)")

label_limit_entry = tk.Label(app, text = "Nhập giới hạn trên dưới a, b")
label_limit_entry.pack()

# Nhập giới hạn dưới 
lower_limit_entry = tk.Entry(app)
lower_limit_entry.pack()

# Nhập giới hạn trên
upper_limit_entry = tk.Entry(app)
upper_limit_entry.pack()

# Nút tính toán
calculate_button = tk.Button(app, text="Tính Đạo Hàm, Tích Phân và Vẽ Đồ Thị", command=calculate_and_plot)
calculate_button.pack()

# Nút tính tích phân xác định
definite_integral_button = tk.Button(app, text="Tính Tích Phân Xác Định", command=calculate_definite_integral)
definite_integral_button.pack()

# Kết quả
result_var = tk.StringVar()
result_label = tk.Label(app, textvariable=result_var)
result_label.pack()

integral_var = tk.StringVar()
integral_label = tk.Label(app, textvariable=integral_var)
integral_label.pack()

definite_integral_var = tk.StringVar()
definite_integral_label = tk.Label(app, textvariable=definite_integral_var)
definite_integral_label.pack()

app.mainloop()