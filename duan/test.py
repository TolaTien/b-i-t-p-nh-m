import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from ttkbootstrap import Style
import pygame
import json
from random import shuffle
import pandas as pd

# Tệp JSON lưu trữ thông tin người chơi và câu hỏi
players_file = "players.json"
questions_file = "cauhoi.py"

# Tải và lưu danh sách người chơi
def load_players():
    try:
        with open(players_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_players(players):
    with open(players_file, "w") as f:
        json.dump(players, f, indent=4)

# Tải và lưu ngân hàng câu hỏi
def load_questions():
    try:
        with open(questions_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_questions(questions):
    with open(questions_file, "w") as f:
        json.dump(questions, f, indent=4)

# Tải dữ liệu ban đầu
players = load_players()
questions = load_questions()

# Tạo cửa sổ ứng dụng chính
manhinh = tk.Tk()
manhinh.title("Quiz Game")
manhinh.geometry("1280x720")
style = Style(theme="cerculean")

# Khởi tạo Pygame
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
pygame.mixer.music.load("nhac.mp3")
pygame.mixer.music.play(-1)

# Biến toàn cục
current_question = 0
score = 0
img = None
selected_category = None
player_name = ""

# Hàm hiển thị màn hình chào mừng
def man_hinh_chao_mung():
    for widget in manhinh.winfo_children():
        widget.destroy()

    tk.Label(manhinh, text="Chào mừng bạn đến với Quiz Game!", font=("Arial", 28), fg="red").pack(pady=50)
    tk.Label(manhinh, text="Tên của bạn:", font=("Arial", 16)).pack(pady=10)

    global player_name_var
    player_name_var = tk.StringVar()
    tk.Entry(manhinh, textvariable=player_name_var, font=("Arial", 16), width=30).pack(pady=10)
    tk.Button(manhinh, text="Tiếp tục", command=man_hinh_the_loai_cau_hoi, font=("Arial", 16), bg="#4CAF50",
              fg="white").pack(pady=40)

# Hàm hiển thị màn hình chọn thể loại câu hỏi
def man_hinh_the_loai_cau_hoi():
    for widget in manhinh.winfo_children():
        widget.destroy()

    global player_name
    player_name = player_name_var.get()

    tk.Label(manhinh, text="Chọn thể loại câu hỏi:", font=("Arial", 24, "bold"), fg="blue").pack(pady=20)

    global category_var
    category_var = tk.StringVar(value=list(questions.keys())[0])

    for category in questions.keys():
        ttk.Radiobutton(manhinh, text=category, variable=category_var, value=category,
                        style="primary.TRadiobutton").pack(pady=15)

    tk.Button(manhinh, text="Bắt đầu Quiz", command=start, font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=30)

# Hàm bắt đầu quiz
def start():
    global selected_category, current_question, score
    selected_category = category_var.get()
    current_question = 0
    score = 0
    shuffle(questions[selected_category])  # Ngẫu nhiên hóa câu hỏi
    display()

# Hàm hiển thị câu hỏi
def display():
    global current_question, img
    for widget in manhinh.winfo_children():
        widget.destroy()

    question_data = questions[selected_category][current_question]

    img_path = question_data.get("image_path", "")
    try:
        pil_image = Image.open(img_path)
        pil_image = pil_image.resize((500, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(pil_image)
        tk.Label(manhinh, image=img).pack(pady=10)
    except:
        tk.Label(manhinh, text="Image not available", font=("Arial", 14)).pack(pady=10)

    tk.Label(manhinh, text=question_data["question"], font=("Arial", 18), wraplength=1000).pack(pady=10)

    button_frame = tk.Frame(manhinh)
    button_frame.pack(pady=20)

    for i, option in enumerate(question_data["options"]):
        tk.Button(
            button_frame, text=option, font=("Arial", 16), bg='#ADD8E6',
            command=lambda opt=option: kiem_tra_dap_an(opt), width=20, height=2
        ).grid(row=i // 2, column=i % 2, padx=10, pady=10)

# Hàm kiểm tra đáp án
def kiem_tra_dap_an(selected_option):
    global current_question, score

    if selected_option == questions[selected_category][current_question]["answer"]:
        score += 1
        correct_sound.play()
        messagebox.showinfo("Đúng!", "Chúc mừng, bạn đã trả lời đúng!")
    else:
        wrong_sound.play()
        messagebox.showinfo("Sai rồi", "Rất tiếc câu trả lời chưa chính xác.")

    current_question += 1
    if current_question < len(questions[selected_category]):
        display()
    else:
        ket_thuc()

# Hàm kết thúc quiz
def ket_thuc():
    global players
    players.append({"name": player_name, "score": score})
    save_players(players)

    for widget in manhinh.winfo_children():
        widget.destroy()

    tk.Label(manhinh, text=f"Kết thúc quiz!\nĐiểm của {player_name}: {score}/{len(questions[selected_category])}",
             font=("Arial", 24), fg="green").pack(pady=20)
    tk.Button(manhinh, text="Xem xếp hạng", command=xem_xep_hang, font=("Arial", 16), bg="#ADD8E6").pack(pady=20)
    tk.Button(manhinh, text="Chơi lại", command=man_hinh_chao_mung, font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(manhinh, text="Thoát", command=manhinh.quit, font=("Arial", 16), bg="#FF6347", fg="white").pack(pady=10)

# Hàm xem xếp hạng
# Hàm xem xếp hạng
def xem_xep_hang():
    for widget in manhinh.winfo_children():
        widget.destroy()

    tk.Label(manhinh, text="Bảng xếp hạng", font=("Arial", 24), fg="blue").pack(pady=20)

    players_sorted = sorted(players, key=lambda x: x["score"], reverse=True)

    for i, player in enumerate(players_sorted):
        tk.Label(manhinh, text=f"{i + 1}. {player['name']} - {player['score']} điểm", font=("Arial", 16)).pack()

    tk.Button(manhinh, text="Quay lại", command=man_hinh_chao_mung, font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Button(manhinh, text="Xuất bảng xếp hạng", command=xuat_bang_xep_hang, font=("Arial", 16), bg="#4CAF50", fg="white").pack(pady=20)
    tk.Button(manhinh, text="Xóa bảng xếp hạng", command=xoa_bang_xep_hang, font=("Arial", 16), bg="#FF6347", fg="white").pack(pady=20)

# Hàm xóa bảng xếp hạng
def xoa_bang_xep_hang():
    global players
    players = []
    save_players(players)
    messagebox.showinfo("Thông báo", "Bảng xếp hạng đã được xóa")
    xem_xep_hang()

# Hàm xuất bảng xếp hạng ra file Excel
def xuat_bang_xep_hang():
    if not players:
        messagebox.showerror("Lỗi", "Không có dữ liệu để xuất!")
        return
    df = pd.DataFrame(players)
    df = df.sort_values(by="score", ascending=False)
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Thành công", f"Bảng xếp hạng đã được xuất ra file {save_path}")

    # Chạy ứng dụng
man_hinh_chao_mung()
manhinh.mainloop()
