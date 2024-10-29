import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # Hàm vẽ đồ thị hàm số
# def plot_function(expr, var, lower_limit=None, upper_limit=None):
#     try:
#         # Chuyển đổi chuỗi biểu thức thành biểu thức SymPy
#         expr = sp.sympify(expr)
#         # x_vals = np.linspace(-10, 10, 400)  # Xác định khoảng giá trị cho x
#         y_vals = [sp.lambdify(var, expr)(x) for x in x_vals]  # Tính giá trị hàm số theo x
#
#         fig, ax = plt.subplots()
#         ax.plot(x_vals, y_vals, label=f'Graph of {expr}')  # Vẽ đồ thị hàm số
#         ax.axhline(0, color='black', linewidth=1)  # Vẽ trục x
#         ax.axvline(0, color='black', linewidth=1)  # Vẽ trục y
#
#         # Nếu có giới hạn dưới và trên, đánh dấu chúng trên đồ thị
#         if lower_limit and upper_limit:
#             lower_limit = float(lower_limit)
#             upper_limit = float(upper_limit)
#
#             # Vẽ các điểm màu đỏ tại giới hạn
#             ax.plot(lower_limit, sp.lambdify(var, expr)(lower_limit), 'ro', label=f'Lower limit: {lower_limit}')
#             ax.plot(upper_limit, sp.lambdify(var, expr)(upper_limit), 'ro', label=f'Upper limit: {upper_limit}')
#
#         ax.legend()  # Hiển thị chú giải
#
#         # Thêm đồ thị vào giao diện Tkinter
#         canvas = FigureCanvasTkAgg(fig, master=frame_plot)
#         canvas.draw()
#         canvas.get_tk_widget().grid(row=0, column=0)
#     except Exception as e:
#         messagebox.showerror("Lỗi", f"Có lỗi khi vẽ đồ thị: {str(e)}")

def plot_function(expr, var):
    x_vals = np.linspace(-7, 7, 400)
    y_vals = [sp.lambdify(var, expr)(x) for x in x_vals]

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f'Graph of {expr}')
    ax.axhline(0, color='black',linewidth=1)
    ax.axvline(0, color='black',linewidth=1)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

# Hàm tính đạo hàm
def calculate_derivative():
    try:
        func_str = entry_function.get()  # Lấy chuỗi hàm số nhập vào
        func = sp.sympify(func_str)  # Chuyển chuỗi hàm thành hàm SymPy
        var = sp.symbols('x')  # Giả sử biến là x
        derivative = sp.diff(func, var)  # Tính đạo hàm
        label_result.config(text=(f"Đạo hàm của hàm {func_str} là: {derivative}"))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Hàm tính tích phân
def calculate_integral():
    try:
        func_str = entry_function.get()  # Lấy chuỗi hàm số nhập vào
        func = sp.sympify(func_str)  # Chuyển chuỗi hàm thành hàm SymPy
        var = sp.symbols('x')  # Giả sử biến là x

        lower_limit = entry_lower.get()  # Giới hạn dưới
        upper_limit = entry_upper.get()  # Giới hạn trên

        if lower_limit and upper_limit:
            # Tính tích phân xác định
            integral = sp.integrate(func, (var, float(lower_limit), float(upper_limit)))
            label_result.config(text=(f"Tích phân của {func_str} từ {lower_limit} đến {upper_limit} là: {integral}"))
        else:
            # Tính tích phân không xác định
            integral = sp.integrate(func, var)
            label_result.config(text=(f"Tích phân không xác định của {func_str} là: {integral}"))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Hàm tìm cực trị
def find_extrema():
    try:
        func_str = entry_function.get()  # Lấy chuỗi hàm số nhập vào
        func = sp.sympify(func_str)  # Chuyển chuỗi hàm thành hàm SymPy
        var = sp.symbols('x')  # Giả sử biến là x

        # Tính đạo hàm của hàm số
        derivative = sp.diff(func, var)
        # Tìm nghiệm của đạo hàm (điểm cực trị)
        critical_points = sp.solveset(derivative, var, domain=sp.S.Reals)

        extrema = []
        for point in critical_points:
            second_derivative = sp.diff(derivative, var).subs(var, point)
            if second_derivative > 0:
                extrema.append(f"Cực tiểu tại x = {point}")
            elif second_derivative < 0:
                extrema.append(f"Cực đại tại x = {point}")
            else:
                extrema.append(f"Điểm yên ngựa tại x = {point}")

        label_result.config(text="\n".join(extrema))

    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Giao diện Tkinter
root = tk.Tk()
root.title("Ứng dụng hỗ trợ học Giải tích")

# Nhập hàm số
label_function = tk.Label(root, text="Nhập hàm số (theo biến x):")
label_function.grid(row=0, column=0)
entry_function = tk.Entry(root, width=30)
entry_function.grid(row=0, column=1)

# Vùng nhập giới hạn tích phân
label_lower = tk.Label(root, text="Giới hạn dưới:")
label_lower.grid(row=1, column=0)
entry_lower = tk.Entry(root, width=10)
entry_lower.grid(row=1, column=1)

label_upper = tk.Label(root, text="Giới hạn trên:")
label_upper.grid(row=2, column=0)
entry_upper = tk.Entry(root, width=10)
entry_upper.grid(row=2, column=1)

# Nút tính tích phân
button_integral = tk.Button(root, text="Tính tích phân", command=calculate_integral)
button_integral.grid(row=3, column=0, columnspan=2)

# Nút tính đạo hàm
button_derivative = tk.Button(root, text="Tính đạo hàm", command=calculate_derivative)
button_derivative.grid(row=4, column=0, columnspan=2)

# Nút tìm cực trị
button_extrema = tk.Button(root, text="Tìm cực trị", command=find_extrema)
button_extrema.grid(row=5, column=0, columnspan=2)

# Nút vẽ đồ thị
button_plot = tk.Button(root, text="Vẽ đồ thị", command=lambda: plot_function(entry_function.get(), sp.symbols('x')))
button_plot.grid(row=6, column=0, columnspan=2)

# Vùng hiển thị đồ thị
frame_plot = tk.Frame(root)
frame_plot.grid(row=7, column=0, columnspan=2)

# Nhãn hiển thị kết quả
label_result = tk.Label(root, text="", justify="left")
label_result.grid(row=8, column=0, columnspan=2)

root.mainloop()#####