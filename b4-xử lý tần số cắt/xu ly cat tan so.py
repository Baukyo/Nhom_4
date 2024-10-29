import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

# Hàm tạo bộ lọc thông thấp
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs  # Tần số Nyquist
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Hàm áp dụng bộ lọc vào tín hiệu
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Các thông số tín hiệu
samplingFrequency = 100
samplingInterval = 1 / samplingFrequency
beginTime = 0
endTime = 10
signal1Frequency = 4  # Tần số tín hiệu cần giữ
signal2Frequency = 7  # Tần số tín hiệu cần lọc bỏ

# Nhập tần số cắt từ người dùng
while True:
    cutoffFrequency = float(input("Nhập tần số cắt cho bộ lọc thông thấp (Hz): "))
    if 0 < cutoffFrequency < (samplingFrequency / 2):
        break
    else:
        print("Tần số cắt phải lớn hơn 0 và nhỏ hơn tần số Nyquist.")

# Tạo thời gian và tín hiệu
time = np.arange(beginTime, endTime, samplingInterval)
amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)
amplitude = amplitude1 + amplitude2  # Tín hiệu tổng

# Áp dụng bộ lọc thông thấp
filtered_amplitude = lowpass_filter(amplitude, cutoffFrequency, samplingFrequency)

# Vẽ đồ thị
figure, axis = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=1)

# Đồ thị 1: Tín hiệu tổng trước khi lọc
axis[0].set_title('Tín hiệu tổng (4 Hz và 7 Hz)')
axis[0].plot(time, amplitude)
axis[0].set_xlabel('Thời gian (s)')
axis[0].set_ylabel('Biên độ')

# Đồ thị 2: Biểu diễn bộ lọc thông thấp
b, a = butter_lowpass(cutoffFrequency, samplingFrequency)
w, h = freqz(b, a, worN=8000)
axis[1].set_title('Đặc tính tần số của bộ lọc thông thấp')
axis[1].plot(0.5 * samplingFrequency * w / np.pi, np.abs(h), 'b')
axis[1].set_xlabel('Tần số (Hz)')
axis[1].set_ylabel('Độ lớn')
axis[1].grid()

# Đồ thị 3: Tín hiệu sau khi lọc
axis[2].set_title(f'Tín hiệu sau khi lọc (Chỉ giữ lại {signal1Frequency} Hz)')
axis[2].plot(time, filtered_amplitude, color='green')
axis[2].set_xlabel('Thời gian (s)')
axis[2].set_ylabel('Biên độ')

plt.tight_layout()
plt.show()

