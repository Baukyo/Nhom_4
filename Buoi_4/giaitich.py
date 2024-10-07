import sympy as sym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

# Hàm tính toán dựa trên lựa chọn của người dùng
def compute():
  try:
    x = sym.Symbol('x')

    # Lấy hàm số do người dùng nhập vào
    function_str = function_entry.get()
    function = sym.sympify(function_str)

    # Lấy lựa chọn người dùng
    choice = operation_var.get()

    # Tính toán theo lựa chọn
    if choice == 'Đạo hàm':
      derivative = sym.diff(function, x)
      derivative_label.config(text=f"Đạo hàm: {sym.pretty(derivative)}")
      integral_label.config(text="")
      antiderivative_label.config(text="")
      extremum_label.config(text="")
    elif choice == 'Tích phân':
      integral = sym.integrate(function, (x, float(lower_entry.get()), float(upper_entry.get())))
      integral_label.config(text=f"Tích phân từ {lower_entry.get()} đến {upper_entry.get()}: {sym.pretty(integral)}")
      derivative_label.config(text="")
      antiderivative_label.config(text="")
      extremum_label.config(text="")
    elif choice == 'Nguyên hàm':
      antiderivative = sym.integrate(function, x)
      antiderivative_label.config(text=f"Nguyên hàm: {sym.pretty(antiderivative)}")
      derivative_label.config(text="")
      integral_label.config(text="")
      extremum_label.config(text="")
    elif choice == 'Cực trị':
      derivative = sym.diff(function, x)
      critical_points = sym.solve(derivative, x)
      extremum_points = [(point, function.subs(x, point)) for point in critical_points]
      extremum_label.config(text=f"Cực trị tại: {extremum_points}")
      derivative_label.config(text="")
      integral_label.config(text="")
      antiderivative_label.config(text="")
    elif choice == 'Giá trị lớn nhất/nhỏ nhất':
      derivative = sym.diff(function, x)
      critical_points = sym.solve(derivative, x)
      y_values = [function.subs(x, point) for point in critical_points]
      max_val = max(y_values)
      min_val = min(y_values)
      extremum_label.config(text=f"Max: {max_val}, Min: {min_val}")
      derivative_label.config(text="")
      integral_label.config(text="")
      antiderivative_label.config(text="")

    # Vẽ đồ thị của hàm số
    plot_function(function)

  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# Hàm vẽ đồ thị của hàm số
def plot_function(function):
  # Tạo mảng các giá trị x
  x_vals = np.linspace(-10, 10, 400)

  # Chuyển hàm sympy sang numpy để vẽ đồ thị
  f_lambdified = sym.lambdify(sym.Symbol('x'), function, modules=['numpy'])

  # Tạo mảng các giá trị y tương ứng với x
  y_vals = f_lambdified(x_vals)

  # Tạo hình vẽ
  fig, ax = plt.subplots()
  ax.plot(x_vals, y_vals, label=f"y = {function}")
  ax.axhline(0, color='black', linewidth=1)
  ax.axvline(0, color='black', linewidth=1)
  ax.set_title("Đồ thị hàm số")
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.grid(True)
  ax.legend()

  # Hiển thị đồ thị trong cửa sổ Tkinter
  for widget in plot_frame.winfo_children():
    widget.destroy()
  canvas = FigureCanvasTkAgg(fig, master=plot_frame)
  canvas.draw()
  canvas.get_tk_widget().pack()


# Giao diện Tkinter
root = tk.Tk()
root.title("Ứng dụng toán học")

# Sử dụng grid layout để sắp xếp giao diện
# Nhãn và ô nhập cho hàm số
tk.Label(root, text="Nhập hàm số (ví dụ: sin(x), cos(x), x**2, ...):").grid(row=0, column=0, padx=10, pady=10,
                                                                            sticky="w")
function_entry = tk.Entry(root, width=30)
function_entry.grid(row=0, column=1, padx=10, pady=10)

# Lựa chọn loại phép tính: Đạo hàm, Tích phân, Nguyên hàm, Cực trị, Giá trị lớn nhất/nhỏ nhất
tk.Label(root, text="Chọn phép tính:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
operation_var = tk.StringVar(value="Đạo hàm")

# Frame để chứa các lựa chọn radio button
operations_frame = tk.Frame(root)
operations_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

operation_radiobuttons = [tk.Radiobutton(operations_frame, text="Đạo hàm", variable=operation_var, value="Đạo hàm"),
  tk.Radiobutton(operations_frame, text="Tích phân", variable=operation_var, value="Tích phân"),
  tk.Radiobutton(operations_frame, text="Nguyên hàm", variable=operation_var, value="Nguyên hàm"),
  tk.Radiobutton(operations_frame, text="Cực trị", variable=operation_var, value="Cực trị"),
  tk.Radiobutton(operations_frame, text="Giá trị lớn nhất/nhỏ nhất", variable=operation_var,
                 value="Giá trị lớn nhất/nhỏ nhất")]

# Sắp xếp các radio button theo hàng ngang
for i, rb in enumerate(operation_radiobuttons):
  rb.grid(row=0, column=i)

# Nhãn và ô nhập cho khoảng tích phân
tk.Label(root, text="Giới hạn dưới (cho tích phân):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
lower_entry = tk.Entry(root)
lower_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Giới hạn trên (cho tích phân):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
upper_entry = tk.Entry(root)
upper_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Nút tính toán
compute_button = tk.Button(root, text="Tính toán", command=compute)
compute_button.grid(row=4, column=0, columnspan=2, pady=10)

# Kết quả tính toán
derivative_label = tk.Label(root, text="")
derivative_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

integral_label = tk.Label(root, text="")
integral_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

antiderivative_label = tk.Label(root, text="")
antiderivative_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Nhãn hiển thị kết quả của nguyên hàm
antiderivative_result_label = tk.Label(root, text="")
antiderivative_result_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Nhãn hiển thị kết quả cực trị
extremum_label = tk.Label(root, text="")
extremum_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Khung hiển thị đồ thị
plot_frame = tk.Frame(root)
plot_frame.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Đảm bảo khung hiển thị đồ thị giãn theo kích thước cửa sổ
root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(1, weight=1)

# Chạy ứng dụng
root.mainloop()
