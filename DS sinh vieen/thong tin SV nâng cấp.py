import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog


def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    try:
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return np.array([])


def search_student(data, student_id):
    """Search for a student's information by ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])


def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])


def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def search_action():
    choice = choice_var.get()
    student_id = id_entry.get()
    subject_name = subject_entry.get()

    if choice == '1':  # Tìm kiếm thông tin sinh viên
        result = search_student(data, student_id)
    elif choice == '2':  # Tìm kiếm điểm môn học
        result = search_subject(data, subject_name)
    elif choice == '3':  # Tính TBC điểm của sinh viên
        result = calculate_average(data, student_id)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)


def statistics_by_class(data):
    """Thống kê điểm theo lớp."""

    subject_name = simpledialog.askstring("Thống kê", "Nhập tên môn học muốn thống kê:")
    if subject_name is None:
        return  # Người dùng nhấn Cancel

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        messagebox.showinfo("Kết quả", f"Không tìm thấy điểm cho môn học {subject_name}.")
        return

    grades = subject_data[:, 3].astype(float)
    average_grade = np.mean(grades)
    max_grade = np.max(grades)
    min_grade = np.min(grades)

    result = f"--- Thống kê điểm môn {subject_name} ---\n"
    result += f"Điểm trung bình: {average_grade:.2f}\n"
    result += f"Điểm cao nhất: {max_grade}\n"
    result += f"Điểm thấp nhất: {min_grade}"
    # ... (thêm kết quả phân loại điểm nếu cần) ...

    messagebox.showinfo("Kết quả", result)


def create_report(data):
    """Tạo báo cáo về thông tin sinh viên và điểm học."""

    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame(data)

    # Chọn tên cột cho DataFrame (nếu cần)
    df.columns = ['ID', 'Họ và tên', 'Môn học', 'Điểm']  # Thay đổi tên cột phù hợp với dữ liệu của bạn

    # Tính trung bình cộng điểm cho từng sinh viên
    student_ids = np.unique(data[:, 0])
    for student_id in student_ids:
        average = calculate_average(data, student_id)
        # Tách thông tin trung bình cộng điểm ra khỏi chuỗi
        avg_str = average.split("là ")[1]
        # Tạo một hàng mới cho DataFrame với thông tin trung bình cộng điểm
        new_row = pd.DataFrame(
            {'ID': [student_id], 'Họ và tên': ['Trung bình cộng điểm'], 'Môn học': ['Tổng'], 'Điểm': [avg_str]})
        df = pd.concat([df, new_row], ignore_index=True)

    # Lưu DataFrame vào file Excel
    file_path_excel = 'report.xlsx'  # Đường dẫn đến file Excel mới
    df.to_excel(file_path_excel, index=False)
    messagebox.showinfo("Thông báo", f"Báo cáo đã được tạo tại {file_path_excel}")


def main():
    global data
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    # Thêm các widget
    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')

    tk.Label(root, text="ID sinh viên:").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    tk.Button(root, text="Tìm kiếm", command=search_action).pack(pady=10)
    tk.Button(root, text="Thống kê điểm theo lớp", command=lambda: statistics_by_class(data)).pack(
        pady=10)  # Thêm nút bấm
    tk.Button(root, text="Tạo báo cáo", command=lambda: create_report(data)).pack(pady=10)  # Thêm nút bấm

    root.mainloop()


if __name__ == "__main__":
    main()