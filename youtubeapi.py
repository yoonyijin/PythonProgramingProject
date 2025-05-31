import tkinter as tk
from tkinter import ttk, messagebox
from googleapiclient.discovery import build
import webbrowser  # 웹 브라우저 열기용

API_KEY = "AIzaSyBAR1RJ6UQneb-FFMdua1Hgqgr_u_1yAYI"

youtube = build('youtube', 'v3', developerKey=API_KEY)

MOOD_KEYWORDS = {
    "행복": "happy upbeat",
    "슬픔": "sad mellow",
    "화남": "angry intense",
    "외로움": "lonely soft",
    "설렘": "excited energetic",
    "지루함": "bored chill",
    "우울": "depressed slow"
}

VALID_GENRES = [
    'pop', 'rock', 'hip hop', 'indie', 'dance', 'electronic', 'jazz', 'classical', 'r&b'
]

def get_recommendation():
    mood = mood_var.get()
    genre = genre_var.get()

    if not mood or not genre:
        messagebox.showerror("오류", "기분과 장르를 모두 선택해주세요.")
        return

    if genre not in VALID_GENRES:
        messagebox.showerror("오류", f"'{genre}'는 유효한 장르가 아니에요!")
        return

    query = f"{MOOD_KEYWORDS[mood]} {genre} music"

    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            maxResults=3,
            type="video",
            videoCategoryId="10",
            safeSearch="moderate"
        )
        response = request.execute()

        videos = response.get("items", [])
        display.delete(0, tk.END)

        if not videos:
            messagebox.showinfo("결과 없음", "조건에 맞는 추천 영상이 없어요 😢\n다른 장르나 기분을 선택해보세요.")
            return

        # 리스트박스에 제목, 채널명, URL을 삽입
        for video in videos:
            title = video['snippet']['title']
            channel = video['snippet']['channelTitle']
            video_id = video['id']['videoId']
            url = f"https://www.youtube.com/watch?v={video_id}"

            display.insert(tk.END, f"{title} - {channel}")
            display.insert(tk.END, url)
            display.insert(tk.END, "")  # 빈 줄

    except Exception as e:
        messagebox.showerror("에러 발생", f"유튜브 API 호출 중 오류가 발생했습니다:\n{e}")

def on_item_double_click(event):
    # 선택한 항목의 인덱스 가져오기
    selection = display.curselection()
    if not selection:
        return
    index = selection[0]

    # URL은 항상 두번째 줄 (인덱스 홀수)
    # 혹은 URL 패턴 검사
    item_text = display.get(index)
    if item_text.startswith("https://www.youtube.com"):
        webbrowser.open(item_text)
    else:
        # 선택한 항목이 제목일 경우, 바로 아래줄(인덱스+1)이 URL일 가능성 있으므로 그걸 열기
        if index + 1 < display.size():
            next_line = display.get(index + 1)
            if next_line.startswith("https://www.youtube.com"):
                webbrowser.open(next_line)

# GUI 설정
root = tk.Tk()
root.title("기분 + 장르 기반 YouTube 음악 추천")
root.geometry("500x500")

mood_var = tk.StringVar()
genre_var = tk.StringVar()

tk.Label(root, text="기분을 선택하세요:").pack(anchor='w', padx=10, pady=(10, 0))
for mood in MOOD_KEYWORDS.keys():
    tk.Radiobutton(root, text=mood, variable=mood_var, value=mood).pack(anchor='w', padx=20)

tk.Label(root, text="장르를 선택하세요:").pack(anchor='w', padx=10, pady=(15, 0))
genre_menu = ttk.Combobox(root, textvariable=genre_var, values=VALID_GENRES, state="readonly")
genre_menu.pack(padx=20, pady=5, fill='x')

tk.Button(root, text="추천받기", command=get_recommendation).pack(pady=10)

display = tk.Listbox(root, width=70, height=15)
display.pack(padx=20, pady=10)
display.bind("<Double-1>", on_item_double_click)  # 더블클릭 이벤트 연결

root.mainloop()
