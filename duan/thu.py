import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
import pygame
from cauhoi import bo_cau_hoi

# Tạo cửa sổ ứng dụng chính
manhinh = tk.Tk()
manhinh.title("Quiz Game")
manhinh.geometry("1280x720")
manhinh.iconbitmap('icon.ico')
style = Style(theme="cerculean")

# Khởi tạo Pygame
pygame.mixer.init()

# Load âm thanh cho câu trả lời đúng và sai
correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
# Load nhạc nền và phát nhạc
pygame.mixer.music.load("nhac.mp3")
pygame.mixer.music.play(-1)

# Biến để theo dõi câu hỏi hiện tại và điểm số
current_question = 0
score = 0
img = None  # Khởi tạo biến để lưu trữ tham chiếu đến ảnh
selected_category = None  # Thể loại câu hỏi đã chọn

# Hàm hiển thị màn hình chào mừng
def man_hinh_chao_mung():
    for widget in manhinh.winfo_children():
        widget.destroy()

    # Tạo label chào mừng
    welcome_label = tk.Label(
        manhinh,
        text="Chào mừng bạn đến với Quiz Game!",
        font=("Arial", 28),
        fg="red"
    )
    welcome_label.pack(pady=50)

    # Tạo nút bắt đầu lớn hơn
    start_button = tk.Button(
        manhinh,
        text="Bắt đầu",
        command=man_hinh_the_loai_cau_hoi,
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        width=15,
        height=2
    )
    start_button.pack(pady=40)

# Hàm bắt đầu quiz
def start():
    global selected_category
    selected_category = category_var.get()  # Lấy thể loại câu hỏi đã chọn
    display()  # Hiển thị câu hỏi đầu tiên

def display():
    global current_question, img

    # Xóa các widget trước đó
    for widget in manhinh.winfo_children():
        widget.destroy()

    # Tạo một frame chính để căn chỉnh câu hỏi và các thành phần
    question_frame = tk.Frame(manhinh)
    question_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Tạo frame trên để hiển thị ảnh và câu hỏi
    top_frame = tk.Frame(question_frame)
    top_frame.pack(pady=20)

    # Hiển thị ảnh câu hỏi (sử dụng Pillow để thay đổi kích thước ảnh)
    img_path = bo_cau_hoi[selected_category][current_question]["image_path"]
    try:
        pil_image = Image.open(img_path)
        pil_image = pil_image.resize((500, 300), Image.LANCZOS)  # Thay đổi kích thước ảnh
        img = ImageTk.PhotoImage(pil_image)
        img_label = tk.Label(top_frame, image=img)
        img_label.pack(pady=10)  # Căn giữa ảnh
    except Exception as e:
        print(f"Error loading image: {e}")
        img_label = tk.Label(top_frame, text="Image not available", font=("Arial", 14))
        img_label.pack(pady=10)

    # Hiển thị câu hỏi
    question_text = tk.Label(top_frame, text=bo_cau_hoi[selected_category][current_question]["question"], font=("Arial", 18), wraplength=1000)
    question_text.pack(pady=10)

    # Hiển thị các lựa chọn dưới dạng các nút bấm
    options = bo_cau_hoi[selected_category][current_question]["options"]
    button_frame = tk.Frame(question_frame)
    button_frame.pack(pady=20)

    for i, option in enumerate(options):
        option_button = tk.Button(
            button_frame, text=option, font=("Arial", 16), bg='#ADD8E6', fg='#000000',
            command=lambda opt=option: kiem_tra_dap_an(opt), width=20, height=2
        )
        option_button.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

    # Định dạng hàng và cột cho các nút
    for i in range(2):  # 2 hàng
        button_frame.grid_rowconfigure(i, weight=1)
    for j in range(2):  # 2 cột
        button_frame.grid_columnconfigure(j, weight=1)

# Hàm kiểm tra đáp án
def kiem_tra_dap_an(selected_option):
    global current_question, score

    if selected_option == bo_cau_hoi[selected_category][current_question]["answer"]:
        score += 1
        correct_sound.play()  # Phát âm thanh đúng
        messagebox.showinfo("Đúng!", "Chúc mừng, bạn đã trả lời đúng!")
    else:
        wrong_sound.play()  # Phát âm thanh sai
        messagebox.showinfo("Sai rồi", "Rất tiếc câu trả lời chưa chính xác.")

    current_question += 1
    if current_question < len(bo_cau_hoi[selected_category]):
        display()
    else:
        ket_thuc()

# Hàm kết thúc quiz và hiển thị điểm số
def ket_thuc():
    for widget in manhinh.winfo_children():
        widget.destroy()

    # Tạo frame chính cho giao diện kết thúc
    end_frame = tk.Frame(manhinh)
    end_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Hiển thị thông báo kết thúc và điểm số
    result_label = tk.Label(
        end_frame,
        text=f"Kết thúc quiz!\nĐiểm của bạn: {score}/{len(bo_cau_hoi[selected_category])}\n",
        font=("Arial", 24, "bold"),
        fg="#4CAF50" if score > len(bo_cau_hoi[selected_category]) // 2 else "#FF6347"  # Màu xanh nếu điểm cao, đỏ nếu thấp
    )
    result_label.pack(pady=20)

    feedback_label = tk.Label(
        end_frame,
        text="Cố lên! Lần sau bạn sẽ làm tốt hơn!" if score <= len(bo_cau_hoi[selected_category]) // 2 else "Chúc mừng! Bạn làm rất tốt!",
        font=("Arial", 18),
        fg="#000000"
    )
    feedback_label.pack(pady=10)

    # Tạo các nút chức năng (Chơi lại và Thoát)
    button_frame = tk.Frame(end_frame)
    button_frame.pack(pady=20)

    Khoi_dong_lai_button = tk.Button(
        button_frame, text="Chơi lại", font=("Arial", 16), bg="#ADD8E6", fg="#000000",
        width=15, height=2, command=Khoi_dong_lai
    )
    Khoi_dong_lai_button.grid(row=0, column=0, padx=10, pady=10)

    exit_button = tk.Button(
        button_frame, text="Thoát", font=("Arial", 16), bg="#FF6347", fg="#FFFFFF",
        width=15, height=2, command=manhinh.quit
    )
    exit_button.grid(row=0, column=1, padx=10, pady=10)

# Hàm khởi động lại quiz
def Khoi_dong_lai():
    global current_question, score
    current_question = 0
    score = 0
    man_hinh_the_loai_cau_hoi()  # Quay lại màn hình chọn thể loại

# Hàm hiển thị màn hình chọn thể loại câu hỏi
def man_hinh_the_loai_cau_hoi():
    for widget in manhinh.winfo_children():
        widget.destroy()

    # Tăng kích thước chữ cho tiêu đề
    category_label = tk.Label(
        manhinh,
        text="Chọn thể loại câu hỏi:",
        font=("Arial", 24, "bold"),  # Chữ to hơn
        fg="blue"
    )
    category_label.pack(pady=20)

    global category_var
    category_var = tk.StringVar(value=list(bo_cau_hoi.keys())[0])

    # Tạo style cho các RadioButton
    style.configure(
        "Custom.TRadiobutton",
        font=("Arial", 15),  # Font lớn hơn
        foreground="blue"
    )

    # Sử dụng style cho các RadioButton
    for category in bo_cau_hoi.keys():
        ttk.Radiobutton(
            manhinh,
            text=category,
            variable=category_var,
            value=category,
            style="primary.TRadiobutton"
        ).pack(pady=15)

    # Tăng kích thước nút bắt đầu quiz
    start_button = tk.Button(
        manhinh,
        text="Bắt đầu Quiz",
        command=start,
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        width=15,
        height=2
    )
    start_button.pack(pady=30)



# Hiển thị màn hình chào mừng khi bắt đầu ứng dụng
man_hinh_chao_mung()

# Bắt đầu vòng lặp chính của ứng dụng
manhinh.mainloop()