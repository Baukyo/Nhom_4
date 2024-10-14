import numpy as np
import pandas as pd
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Initialize the Tkinter window
root = tk.Tk()
root.title("Dự đoán Kết quả Học tập")
root.geometry("500x700")

# Global variables for data and model
df = None
model = None
X_train, X_test, y_train, y_test = None, None, None, None


# Function to load the dataset
def load_data():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được tải thành công!")
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn file dữ liệu.")


# Function to train the model
def train_model():
    global model, X_train, X_test, y_train, y_test
    if df is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước.")
        return

    # Select features and target variable
    x = array(df.iloc[:, 0:5]).astype(np.float64)
    y = array(df.iloc[:, 5]).astype(np.float64)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Get selected algorithm from ComboBox
    selected_algorithm = algorithm_combobox.get()

    # Initialize the model based on selected algorithm
    if selected_algorithm == "KNN":
        model = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
    elif selected_algorithm == "Linear Regression":
        model = LinearRegression()
    elif selected_algorithm == "Decision Tree":
        model = DecisionTreeRegressor()
    elif selected_algorithm == "SVR":
        model = SVR(kernel='linear')
    else:
        messagebox.showerror("Lỗi", "Thuật toán không hợp lệ.")
        return

    # Train the model
    model.fit(X_train, y_train)
    messagebox.showinfo("Thông báo", "Đã huấn luyện mô hình thành công!")


# Function to test the model and show errors
def test_model():
    global model, X_test, y_test
    if model is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện mô hình trước.")
        return

    # Thực hiện dự đoán
    y_predict = model.predict(X_test)

    # Tính toán sai số
    mse = mean_squared_error(y_test, y_predict)
    mae = mean_absolute_error(y_test, y_predict)
    rmse = np.sqrt(mse)

    # Hiển thị sai số
    messagebox.showinfo("Sai số", f"MSE: {mse:.2f}\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}")

    # So sánh sai số của các thuật toán khác nhau
    algorithms = {
        "KNN": neighbors.KNeighborsRegressor(n_neighbors=3, p=2),
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "SVR": SVR(kernel='linear')
    }

    errors = {}

    for name, algo in algorithms.items():
        algo.fit(X_train, y_train)
        y_pred_algo = algo.predict(X_test)
        mse_algo = mean_squared_error(y_test, y_pred_algo)
        errors[name] = mse_algo

    # Biểu đồ so sánh sai số giữa các thuật toán
    fig, ax = plt.subplots()
    ax.bar(errors.keys(), errors.values(), color=['blue', 'green', 'red', 'purple'])
    ax.set_title("So sánh sai số MSE giữa các thuật toán")
    ax.set_ylabel("MSE")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Function to predict a new student's score
def predict_score():
    global model
    if model is None:
        messagebox.showwarning("Cảnh báo", "Vui lòng huấn luyện mô hình trước.")
        return
    try:
        # Get input values
        hours = float(entry_hours.get())
        scores = float(entry_scores.get())
        activities = float(entry_activities.get())
        sleep = float(entry_sleep.get())
        papers = float(entry_papers.get())

        # Ensure no negative values
        if any(v < 0 for v in [hours, scores, activities, sleep, papers]):
            raise ValueError("Giá trị nhập vào không được âm.")

        # Prepare input data
        input_data = np.array([[hours, scores, activities, sleep, papers]])

        # Predict and display result
        prediction = model.predict(input_data)[0]
        prediction = max(0, min(100, prediction))  # Limit between 0 and 100
        result_label.config(text=f"Điểm dự đoán: {prediction:.2f}")

        # Clear inputs
        clear_inputs()

    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))


# Clear inputs after prediction
def clear_inputs():
    entry_hours.delete(0, tk.END)
    entry_scores.delete(0, tk.END)
    entry_activities.delete(0, tk.END)
    entry_sleep.delete(0, tk.END)
    entry_papers.delete(0, tk.END)


# UI for loading data
load_button = tk.Button(root, text="Tải dữ liệu CSV", command=load_data)
load_button.pack(pady=10)

# UI for selecting algorithm
algorithm_label = tk.Label(root, text="Chọn thuật toán:")
algorithm_label.pack(pady=5)
algorithm_combobox = ttk.Combobox(root, values=["KNN", "Linear Regression", "Decision Tree", "SVR"])
algorithm_combobox.pack(pady=5)
algorithm_combobox.current(0)  # Set default selection

# UI for training the model
train_button = tk.Button(root, text="Huấn luyện mô hình", command=train_model)
train_button.pack(pady=10)

# UI for testing the model
test_button = tk.Button(root, text="Kiểm tra mô hình", command=test_model)
test_button.pack(pady=10)

# UI for entering new student data and predicting
label_hours = tk.Label(root, text="Giờ học:")
label_hours.pack(pady=5)
entry_hours = tk.Entry(root)
entry_hours.pack(pady=5)

label_scores = tk.Label(root, text="Điểm trước:")
label_scores.pack(pady=5)
entry_scores = tk.Entry(root)
entry_scores.pack(pady=5)

label_activities = tk.Label(root, text="Hoạt động ngoại khóa:")
label_activities.pack(pady=5)
entry_activities = tk.Entry(root)
entry_activities.pack(pady=5)

label_sleep = tk.Label(root, text="Giờ ngủ:")
label_sleep.pack(pady=5)
entry_sleep = tk.Entry(root)
entry_sleep.pack(pady=5)

label_papers = tk.Label(root, text="Số đề đã luyện:")
label_papers.pack(pady=5)
entry_papers = tk.Entry(root)
entry_papers.pack(pady=5)

# Button to predict score
predict_button = tk.Button(root, text="Dự đoán kết quả", command=predict_score)
predict_button.pack(pady=20)

# Label to display prediction result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
