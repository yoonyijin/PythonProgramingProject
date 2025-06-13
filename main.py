# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from func1_youtube import get_recommendation
from func2_event import on_item_double_click
from func3_data import MOOD_KEYWORDS, VALID_GENRES

def on_recommend():
    mood = mood_var.get()
    genre = genre_var.get()
    if not mood:
        messagebox.showerror("오류", "기분을 선택해주세요.")
        return
    if genre not in VALID_GENRES:
        messagebox.showerror("오류", f"'{genre}'는 유효한 장르가 아니에요!")
        return
    get_recommendation(mood_var, genre_var, display)

root = tk.Tk()
root.title("기분 + 장르 기반 YouTube 음악 추천")
root.geometry("500x550")

mood_var = tk.StringVar()
genre_var = tk.StringVar()

tk.Label(root, text="기분을 선택하세요:").pack(anchor='w', padx=10, pady=(10, 0))
for mood in MOOD_KEYWORDS.keys():
    tk.Radiobutton(root, text=mood, variable=mood_var, value=mood).pack(anchor='w', padx=20)

tk.Label(root, text="장르를 선택하세요:").pack(anchor='w', padx=10, pady=(15, 0))
genre_menu = ttk.Combobox(root, textvariable=genre_var, values=VALID_GENRES, state="readonly")
genre_menu.pack(padx=20, pady=5, fill='x')
genre_menu.current(0)  # 기본 장르 선택

tk.Button(root, text="추천받기 🎵", command=on_recommend).pack(pady=10)

display = tk.Listbox(root, width=70, height=15)
display.pack(padx=20, pady=10)
display.bind("<Double-1>", lambda event: on_item_double_click(display))

root.mainloop()
