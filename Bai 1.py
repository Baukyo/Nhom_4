import numpy as np
import tkinter as tk
from tkinter import messagebox


# Hàm giải hệ phương trình tuyến tính
def giai_he_pt(A, B):
    try:
        rank_A = np.linalg.matrix_rank(A)
        augmented_matrix = np.column_stack((A, B))  # Ma trận mở rộng
        rank_augmented = np.linalg.matrix_rank(augmented_matrix)

        if rank_A < rank_augmented:
            return "Vô nghiệm"
        elif rank_A == rank_augmented < len(A):
            return "Vô số nghiệm"
        else:
            # Trường hợp nghiệm duy nhất
            A_inv = np.linalg.inv(A)
            X = np.dot(A_inv, B)
            return X
    except np.linalg.LinAlgError:
        return None



# Hàm xử lý khi nhấn nút "Giải"
def solve_system():
    try:
        n = int(entry_n.get())  # số phương trình và số ẩn
        A = np.zeros((n, n))  # ma trận hệ số
        B = np.zeros(n)  # ma trận hằng số

        # Lấy dữ liệu từ các ô nhập
        for i in range(n):
            for j in range(n):
                A[i, j] = float(entries_A[i][j].get())
            B[i] = float(entries_B[i].get())

        # Giải hệ phương trình
        result = giai_he_pt(A, B)
        if isinstance(result, str):
            messagebox.showerror("Kết quả", result)
        else:
            result_str = ', '.join([f"x{i + 1} = {result[i]:.2f}" for i in range(n)])
            messagebox.showinfo("Kết quả", f"Nghiệm của hệ là: {result_str}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")


# Hàm để tạo các ô nhập cho ma trận hệ số và hằng số
def create_input_fields():
    try:
        n = int(entry_n.get())  # số phương trình và số ẩn
        for widget in frame_inputs.winfo_children():
            widget.destroy()  # Xóa các ô nhập trước đó

        global entries_A, entries_B
        entries_A = []
        entries_B = []

        # Tạo ô nhập cho ma trận hệ số A
        for i in range(n):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(frame_inputs, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries_A.append(row_entries)

        # Tạo ô nhập cho ma trận hằng số B
        for i in range(n):
            entry = tk.Entry(frame_inputs, width=5)
            entry.grid(row=i, column=n, padx=5, pady=5)
            entries_B.append(entry)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số phương trình hợp lệ")
# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải hệ phương trình tuyến tính")

# Frame cho nhập số phương trình và số ẩn
frame_top = tk.Frame(root)
frame_top.pack(padx=10, pady=10)

label_n = tk.Label(frame_top, text="Số phương trình và số ẩn:")
label_n.pack(side=tk.LEFT)

entry_n = tk.Entry(frame_top, width=5)
entry_n.pack(side=tk.LEFT, padx=5)

btn_create_fields = tk.Button(frame_top, text="Tạo", command=create_input_fields)
btn_create_fields.pack(side=tk.LEFT, padx=5)

# Frame cho các ô nhập hệ số và hằng số
frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=10, pady=10)

# Nút giải hệ phương trình
btn_solve = tk.Button(root, text="Giải", command=solve_system)
btn_solve.pack(padx=10, pady=10)

# Chạy vòng lặp giao diện
root.mainloop()