# func1_youtube.py
import tkinter as tk
from tkinter import messagebox
from googleapiclient.discovery import build

API_KEY = "AIzaSyBAR1RJ6UQneb-FFMdua1Hgqgr_u_1yAYI"
youtube = build('youtube', 'v3', developerKey=API_KEY)

from func3_data import MOOD_KEYWORDS

def get_recommendation(mood_var, genre_var, display):
    mood = mood_var.get()
    genre = genre_var.get()

    if not mood or not genre:
        messagebox.showerror("오류", "기분과 장르를 모두 선택해주세요.")
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
            messagebox.showinfo("결과 없음", "조건에 맞는 추천 영상이 없어요 😢")
            return

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
