import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Biến toàn cục để lưu dữ liệu và thuật toán
X_train, X_test, y_train, y_test = None, None, None, None
knn = None
algorithm = 'regression'  # Mặc định sử dụng hồi quy
df = None  # Khởi tạo biến df toàn cục

# Hàm tải dữ liệu từ file CSV
def load_data():
    global X_train, X_test, y_train, y_test, knn, df  # Thêm df vào danh sách biến toàn cục
    file_path = filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)

            # Chuẩn bị dữ liệu
            x = np.array(df.iloc[:, 0:5]).astype(np.float64)  # Chọn cột dữ liệu về đặc điểm sinh viên
            y = np.array(df.iloc[:, 5]).astype(np.float64)    # Chọn cột điểm

            # Chia dữ liệu thành tập huấn luyện và kiểm tra
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

            # Huấn luyện mô hình KNN
            if algorithm == 'regression':
                knn = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
            else:
                knn = neighbors.KNeighborsClassifier(n_neighbors=3, p=2)
                
            knn.fit(X_train, y_train)

            messagebox.showinfo("Thông báo", "Dữ liệu huấn luyện và kiểm tra đã được tải.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

# Hàm dự đoán điểm dựa trên dữ liệu người dùng nhập
def predict_score():
    try:
        input_data = [float(entry1.get()), float(entry2.get()), float(entry3.get()), float(entry4.get()), float(entry5.get())]
        
        # Thực hiện dự đoán
        prediction = knn.predict([input_data])[0]
        messagebox.showinfo("Dự đoán", f"Điểm dự đoán: {prediction:.2f}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập dữ liệu hợp lệ!")

# Hàm hiển thị kết quả
def show_results():
    if knn is None:
        messagebox.showerror("Lỗi", "Chưa có mô hình được huấn luyện.")
        return
    y_predict = knn.predict(X_test)
    
    mse_score = mean_squared_error(y_test, y_predict)
    mae_score = mean_absolute_error(y_test, y_predict)
    rmse_score = np.sqrt(mse_score)
    
    result_message = f"MSE Score: {mse_score:.2f}\nMAE Score: {mae_score:.2f}\nRMSE: {rmse_score:.2f}"
    messagebox.showinfo("Kết quả đánh giá mô hình", result_message)

# Hàm vẽ biểu đồ thống kê cho từng thuộc tính
def plot_statistics():
    global df  # Đảm bảo sử dụng biến df toàn cục
    if df is None:
        messagebox.showerror("Lỗi", "Chưa có dữ liệu nào được tải.")
        return
    
    features = df.columns[:-1]  # Lấy tất cả các cột trừ cột điểm
    plt.figure(figsize=(15, 10))

    for i, feature in enumerate(features):
        plt.subplot(2, 3, i + 1)  # Chia lưới thành 2 hàng, 3 cột
        plt.hist(df[feature], bins=10, color='skyblue', edgecolor='black')
        plt.title(f'Thống kê cho {feature}')
        plt.xlabel(feature)
        plt.ylabel('Số lượng')

    plt.tight_layout()
    plt.show()

# Vẽ biểu đồ kết quả dự đoán so với dữ liệu thực tế
def plot_results():
    if knn is None:
        messagebox.showerror("Lỗi", "Chưa có mô hình được huấn luyện.")
        return
    y_predict = knn.predict(X_test)
    
    plt.plot(range(0, len(y_test)), y_test, 'ro', label='Dữ liệu thực tế')
    plt.plot(range(0, len(y_predict)), y_predict, 'bo', label='Dữ liệu dự đoán')
    for i in range(0, len(y_test)):
        plt.plot([i, i], [y_test[i], y_predict[i]], 'green')
    plt.title('KNN Result')
    plt.xlabel('Index')
    plt.ylabel('Performance Index')
    plt.legend()
    plt.grid(True)
    plt.show()

# Hàm thay đổi thuật toán
def select_algorithm(selected_algorithm):
    global algorithm
    algorithm = selected_algorithm

# Thiết kế giao diện với Tkinter
root = tk.Tk()
root.title("Ứng dụng Dự đoán Kết quả Học tập")

tk.Label(root, text="Thông tin sinh viên").grid(row=0, columnspan=2)

tk.Label(root, text="Hours Studied").grid(row=1)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1)

tk.Label(root, text="Previous Scores").grid(row=2)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=1)

tk.Label(root, text="Extracurricular Activities").grid(row=3)
entry3 = tk.Entry(root)
entry3.grid(row=3, column=1)

tk.Label(root, text="Sleep Hours").grid(row=4)
entry4 = tk.Entry(root)
entry4.grid(row=4, column=1)

tk.Label(root, text="Sample Question Papers Practiced").grid(row=5)
entry5 = tk.Entry(root)
entry5.grid(row=5, column=1)

# Menu chọn thuật toán
algorithm_menu = tk.StringVar(value='regression')
tk.Label(root, text="Chọn thuật toán:").grid(row=6, column=0)
tk.Radiobutton(root, text="KNN Regression", variable=algorithm_menu, value='regression', command=lambda: select_algorithm('regression')).grid(row=6, column=1)
tk.Radiobutton(root, text="KNN Classification", variable=algorithm_menu, value='classification', command=lambda: select_algorithm('classification')).grid(row=7, column=1)

# Nút tải dữ liệu
load_button = tk.Button(root, text="Tải dữ liệu", command=load_data)
load_button.grid(row=8, columnspan=2)

# Nút dự đoán
predict_button = tk.Button(root, text="Dự đoán", command=predict_score)
predict_button.grid(row=9, columnspan=2)

# Nút hiển thị kết quả
results_button = tk.Button(root, text="Hiển thị kết quả", command=show_results)
results_button.grid(row=10, columnspan=2)

# Nút vẽ biểu đồ thống kê
statistics_button = tk.Button(root, text="Vẽ biểu đồ thống kê", command=plot_statistics)
statistics_button.grid(row=11, columnspan=2)

# Nút vẽ biểu đồ kết quả
plot_button = tk.Button(root, text="Vẽ biểu đồ kết quả", command=plot_results)
plot_button.grid(row=12, columnspan=2)

# Chạy ứng dụng
root.mainloop()
