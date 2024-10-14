import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error


def chon_tep():
    global df
    duong_dan_tep = filedialog.askopenfilename(filetypes=[("Tệp CSV", "*.csv")])
    if duong_dan_tep:
        try:
            df = pd.read_csv(duong_dan_tep)
            nhan_tep.config(text=duong_dan_tep)
            nut_huan_luyen.config(state="normal")
        except Exception as e:
            print(f"Lỗi đọc tệp: {e}")
            nhan_tep.config(text="Lỗi đọc tệp")


def huan_luyen_mo_hinh():
    global X_train, X_test, y_train, y_test, model, y_predict
    try:
        X = np.array(df.iloc[:, :-1]).astype(np.float64)  # Đặc trưng (tất cả các cột trừ cột cuối)
        y = np.array(df.iloc[:, -1:]).astype(np.float64)  # Mục tiêu (cột cuối cùng)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

        thuat_toan = bien_thuat_toan.get()
        if thuat_toan == "KNN":
            model = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
        elif thuat_toan == "Hồi quy tuyến tính":
            model = LinearRegression()

        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)

        mse = mean_squared_error(y_test, y_predict)
        mae = mean_absolute_error(y_test, y_predict)
        rmse = np.sqrt(mse)

        nhan_mse.config(text=f"MSE: {mse:.2f}")
        nhan_mae.config(text=f"MAE: {mae:.2f}")
        nhan_rmse.config(text=f"RMSE: {rmse:.2f}")

        so_luong_loi = {
            "<1": np.sum(abs(y_test - y_predict) < 1),
            "1-2": np.sum((abs(y_test - y_predict) >= 1) & (abs(y_test - y_predict) < 2)),
            ">2": np.sum(abs(y_test - y_predict) >= 2)
        }

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(range(len(y_test)), y_test, 'ro', label='Dữ liệu gốc')
        plt.plot(range(len(y_predict)), y_predict, 'bo', label='Dữ liệu dự đoán')
        for i in range(len(y_test)):
            plt.plot([i, i], [y_test[i], y_predict[i]], 'g')
        plt.title('Thực tế vs. Dự đoán')
        plt.legend()

        plt.subplot(1, 2, 2)
        nhan = so_luong_loi.keys()
        kich_thuoc = so_luong_loi.values()
        plt.bar(nhan, kich_thuoc)
        plt.title('Phân bố lỗi')
        plt.show()

        nut_du_doan.config(state="normal")

    except Exception as e:
        print(f"Lỗi trong quá trình huấn luyện: {e}")
        nhan_mse.config(text="Lỗi huấn luyện")


def du_doan_du_lieu_moi():
    try:
        gio_hoc = float(nhap_gio_hoc.get())
        diem_truoc = float(nhap_diem_truoc.get())
        hoat_dong_ngoai_khoa = float(nhap_hoat_dong_ngoai_khoa.get())  # Chuyển đổi sang dạng số (ví dụ: 1 cho Có, 0 cho Không)
        gio_ngu = float(nhap_gio_ngu.get())
        so_bai_tap = float(nhap_so_bai_tap.get())

        du_lieu_moi = np.array([gio_hoc, diem_truoc, hoat_dong_ngoai_khoa, gio_ngu, so_bai_tap]).reshape(1, -1)
        du_doan = model.predict(du_lieu_moi)
        nhan_du_doan.config(text=f"Dự đoán: {du_doan[0][0]:.2f}")

    except ValueError:
        nhan_du_doan.config(text="Định dạng đầu vào không hợp lệ. Vui lòng nhập số.")
    except Exception as e:
        print(f"Lỗi dự đoán: {e}")
        nhan_du_doan.config(text="Lỗi dự đoán")



root = tk.Tk()
root.title("Dự đoán Điểm Sinh Viên")


nhan_tep = tk.Label(root, text="Chưa chọn tệp")
nhan_tep.pack()

nut_chon_tep = tk.Button(root, text="Chọn tệp CSV", command=chon_tep)
nut_chon_tep.pack()


bien_thuat_toan = tk.StringVar(value="KNN")  # Thuật toán mặc định

khung_thuat_toan = tk.Frame(root)
khung_thuat_toan.pack()

nut_chon_knn = tk.Radiobutton(khung_thuat_toan, text="KNN", variable=bien_thuat_toan, value="KNN")
nut_chon_knn.pack(side=tk.LEFT)

nut_chon_hoi_quy_tuyen_tinh = tk.Radiobutton(khung_thuat_toan, text="Hồi quy tuyến tính", variable=bien_thuat_toan, value="Hồi quy tuyến tính")
nut_chon_hoi_quy_tuyen_tinh.pack(side=tk.LEFT)


nut_huan_luyen = tk.Button(root, text="Huấn luyện mô hình", command=huan_luyen_mo_hinh, state="disabled")
nut_huan_luyen.pack()


nhan_mse = tk.Label(root, text="")
nhan_mse.pack()

nhan_mae = tk.Label(root, text="")
nhan_mae.pack()

nhan_rmse = tk.Label(root, text="")
nhan_rmse.pack()


khung_nhap_du_lieu = tk.LabelFrame(root, text="Nhập dữ liệu mới")
khung_nhap_du_lieu.pack(pady=10)

nhan_gio_hoc = tk.Label(khung_nhap_du_lieu, text="Giờ học:")
nhan_gio_hoc.grid(row=0, column=0)
nhap_gio_hoc = tk.Entry(khung_nhap_du_lieu)
nhap_gio_hoc.grid(row=0, column=1)

nhan_diem_truoc = tk.Label(khung_nhap_du_lieu, text="Điểm trước:")
nhan_diem_truoc.grid(row=1, column=0)
nhap_diem_truoc = tk.Entry(khung_nhap_du_lieu)
nhap_diem_truoc.grid(row=1, column=1)


nhan_hoat_dong_ngoai_khoa = tk.Label(khung_nhap_du_lieu, text="Hoạt động ngoại khóa (1 cho Có, 0 cho Không):")
nhan_hoat_dong_ngoai_khoa.grid(row=2, column=0)
nhap_hoat_dong_ngoai_khoa = tk.Entry(khung_nhap_du_lieu)
nhap_hoat_dong_ngoai_khoa.grid(row=2, column=1)

nhan_gio_ngu = tk.Label(khung_nhap_du_lieu, text="Giờ ngủ:")
nhan_gio_ngu.grid(row=3, column=0)
nhap_gio_ngu = tk.Entry(khung_nhap_du_lieu)
nhap_gio_ngu.grid(row=3, column=1)

nhan_so_bai_tap = tk.Label(khung_nhap_du_lieu, text="Số bài tập đã làm:")
nhan_so_bai_tap.grid(row=4, column=0)
nhap_so_bai_tap = tk.Entry(khung_nhap_du_lieu)
nhap_so_bai_tap.grid(row=4, column=1)


nut_du_doan = tk.Button(root, text="Dự đoán", command=du_doan_du_lieu_moi, state="disabled")
nut_du_doan.pack()

nhan_du_doan = tk.Label(root, text="")
nhan_du_doan.pack()

root.mainloop()