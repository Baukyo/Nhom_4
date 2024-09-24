import numpy as np
import tkinter as tk
from tkinter import messagebox


# Hàm để giải hệ phương trình
def solve_system():
  try:
    # Lấy giá trị của n (số phương trình)
    n = int(entry_n.get())

    # Khởi tạo ma trận A và vector B từ các entry
    A = []
    B = []

    for i in range(n):
      row = []
      for j in range(n):
        entry = entries_A[i][j]
        row.append(float(entry.get()))
      A.append(row)

    for i in range(n):
      entry = entries_B[i]
      B.append(float(entry.get()))

    A = np.array(A)
    B = np.array(B)

    # Kiểm tra tính khả nghịch của ma trận A
    rank_A = np.linalg.matrix_rank(A)
    augmented_matrix = np.hstack([A, B.reshape(-1, 1)])
    rank_augmented = np.linalg.matrix_rank(augmented_matrix)

    if rank_A < n:
      if rank_A == rank_augmented:
        # Hệ có vô số nghiệm
        messagebox.showinfo("Kết quả", "Hệ phương trình có vô số nghiệm.")
      else:
        # Hệ vô nghiệm
        messagebox.showerror("Kết quả", "Hệ phương trình vô nghiệm.")
    else:
      # Giải hệ phương trình nếu ma trận A khả nghịch
      X = np.linalg.solve(A, B)

      # Hiển thị nghiệm dưới dạng ma trận n x 1
      # result_text = "Ma trận A ({}x{}):\n".format(n, n)
      # result_text += str(A) + "\n\n"
      #
      # result_text += "Vector B ({}x1):\n".format(n)
      # result_text += str(B.reshape(n, 1)) + "\n\n"

      result_text = "Nghiệm X ({}x1):\n".format(n)
      result_text += str(X.reshape(n, 1)) + "\n"

      label_result.config(text=result_text)

  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số.")
  except Exception as e:
    messagebox.showerror("Lỗi", str(e))


# Hàm để tạo các ô nhập liệu ma trận A và B
def create_entries():
  try:
    n = int(entry_n.get())

    # Xóa các widget cũ nếu có
    for widget in frame_A.winfo_children():
      widget.destroy()
    for widget in frame_B.winfo_children():
      widget.destroy()

    global entries_A, entries_B
    entries_A = []
    entries_B = []

    # Tạo các ô nhập liệu cho ma trận A
    tk.Label(frame_A, text="Ma trận A ({}x{}):".format(n, n)).pack()
    for i in range(n):
      row_entries = []
      row_frame = tk.Frame(frame_A)
      row_frame.pack()
      for j in range(n):
        entry = tk.Entry(row_frame, width=5)
        entry.pack(side=tk.LEFT, padx=5, pady=5)
        row_entries.append(entry)
      entries_A.append(row_entries)

    # Tạo các ô nhập liệu cho vector B
    tk.Label(frame_B, text="Vector B ({}x1):".format(n)).pack()
    for i in range(n):
      entry = tk.Entry(frame_B, width=5)
      entry.pack(padx=5, pady=5)
      entries_B.append(entry)

  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số.")

# def reset():
#   n = int(entry_n.get())
#
#   # Khởi tạo ma trận A và vector B từ các entry
#   A = []
#   B = []
#
#   for i in range(n):
#     row = []
#     for j in range(n):
#       entry = entries_A[i][j]
#       row.append(float(entry.get()))
#     A.append(row)
#
#   for i in range(n):
#     entry = entries_B[i]
#     B.append(float(entry.get()))
#
#   A = np.array(A)
#   B = np.array(B)
# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Giải hệ phương trình tuyến tính")

# Nhập số phương trình n
tk.Label(root, text="Nhập số phương trình (n):").pack(pady=10)
entry_n = tk.Entry(root)
entry_n.pack(pady=5)

# Nút để tạo ma trận A và vector B
button_create = tk.Button(root, text="Tạo ma trận và vector", command=create_entries)
button_create.pack(pady=10)

# Khung chứa các phần nhập liệu cho ma trận A và vector B
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Khung cho ma trận A
frame_A = tk.Frame(frame_input)
frame_A.pack(side=tk.LEFT, padx=20)

# Khung cho vector B
frame_B = tk.Frame(frame_input)
frame_B.pack(side=tk.LEFT, padx=20)

# Nút để giải hệ phương trình
button_solve = tk.Button(root, text="Giải hệ phương trình", command=solve_system)
button_solve.pack(pady=10)

# Nhãn hiển thị kết quả
label_result = tk.Label(root, text="", justify="left")
label_result.pack(pady=10)

# # Nút để reset
# button_solve = tk.Button(root, text="RESET", command=reset)
# button_solve.pack(pady=10)
# Chạy vòng lặp chính
root.mainloop()
