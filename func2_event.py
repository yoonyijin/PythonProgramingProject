# func2_event.py
import webbrowser

def on_item_double_click(display):
    selection = display.curselection()
    if not selection:
        return
    index = selection[0]
    item_text = display.get(index)

    if item_text.startswith("https://www.youtube.com"):
        webbrowser.open(item_text)
    else:
        if index + 1 < display.size():
            next_line = display.get(index + 1)
            if next_line.startswith("https://www.youtube.com"):
                webbrowser.open(next_line)
