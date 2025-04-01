import serial
import time
import csv
from datetime import datetime

# Cấu hình cổng Serial
SERIAL_PORT = 'COM7'  # Thay 'COM7' bằng cổng mà Arduino của bạn đang kết nối
BAUD_RATE = 9600
TIMEOUT = 1  # Giây

# Tên file CSV để lưu dữ liệu (Sử dụng đường dẫn tuyệt đối để đảm bảo file được tạo ở đúng vị trí)
CSV_FILE = r'D:\Collect_AI\code_c\co2_data.csv'

def main():
    try:
        # Mở kết nối Serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Kết nối với {SERIAL_PORT} thành công.")
        time.sleep(2)  # Đợi Arduino khởi động

        # Mở file CSV để ghi
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'co2'])  # Ghi header
            file.flush()  # Đảm bảo header được ghi ngay lập tức

            while True:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    if line.startswith("CO2,"):
                        try:
                            # Giả sử dòng dữ liệu là "CO2,ppm"
                            parts = line.split(',')
                            if len(parts) == 2:
                                ppm = parts[1]

                                # Lấy thời gian hiện tại
                                current_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

                                # Ghi vào file CSV
                                writer.writerow([current_time, ppm])
                                file.flush()  # Ghi dữ liệu ngay lập tức vào file
                                print(f"{current_time}, {ppm} ppm")
                        except Exception as e:
                            print(f"Lỗi khi xử lý dòng: {line}. Error: {e}")
                time.sleep(0.1)  # Đợi 100ms trước khi kiểm tra lại
    except serial.SerialException as e:
        print(f"Lỗi kết nối Serial: {e}")
    except KeyboardInterrupt:
        print("Đã dừng chương trình.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
