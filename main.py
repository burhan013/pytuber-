import pathlib
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from logic import build_ui
from pytubefix import YouTube, Playlist

# Base download directory
BASE_DOWNLOAD_DIR = pathlib.Path(__file__).parent / "Downloads"
BASE_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

#Converts seconds to M:SS (if hours H:MM:SS).
def format_duration(seconds):
    total = int(seconds)
    m, s = divmod(total, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:d}" if h else f"{m:d}:{s:02d}"


def main():
    window = ttk.Window(title="Kebab", themename="superhero")
    window.geometry("1200x800")

    widgets = build_ui(window)
    theme = widgets["theme"]
    download_type = widgets["download_type"]
    url_entry = widgets["url_entry"]
    clear_btn = widgets["clear_btn"]
    download_btn = widgets["download_btn"]
    submit_btn = widgets["submit_btn"]
    tree = widgets["loaded_tree"]
    video_label = widgets["video_label"]

    style = ttk.Style()
    theme.trace_add("write", lambda *_: style.theme_use(theme.get()))

    # Place overall progress bar under the buttons
    center = video_label.master.master
    prog_bar = ttk.Progressbar(
        center, bootstyle="success", mode="determinate", length=300
    )
    prog_bar.pack(pady=(10, 0))

    def load_thumbnail(url):
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            img = Image.open(resp.raw).resize((320, 180))
            photo = ImageTk.PhotoImage(img)
            video_label.configure(image=photo)
            video_label.image = photo
        except Exception as e:
            print("Thumbnail load error:", e)

    def clear_all():
        url_entry.delete(0, tk.END)
        video_label.configure(image='')
        video_label.image = None
        for item in tree.get_children():
            tree.delete(item)
        prog_bar.configure(value=0)

    clear_btn.configure(command=clear_all)

    # Pytube progress callback
    def progress_fn(stream, chunk, bytes_remaining):
        total = stream.filesize or 1
        done = total - bytes_remaining
        percent = int(done / total * 100)
        prog_bar.configure(maximum=100, value=percent)
        window.update_idletasks()

    def on_add_to_list():
        url = url_entry.get().strip()
        try:
            vids = Playlist(url).videos if download_type.get() == "playlist" else [YouTube(url)]
            tree.delete(*tree.get_children())
            for idx, yt in enumerate(vids, start=1):
                tree.insert(
                    "", "end",
                    values=(str(idx), yt.title, format_duration(yt.length)),
                    tags=(yt.watch_url,)
                )
            load_thumbnail(vids[0].thumbnail_url)
        except Exception as e:
            Messagebox.show_error("Invalid Input (Mixes don't work, Has to be Public playlist)", str(e))

    submit_btn.configure(command=on_add_to_list)

    def on_download():
        vids = tree.get_children()
        if not vids:
            Messagebox.show_info("No videos", "Add videos before downloading.")
            return

        # Determine if audio-only for playlist downloads via dialog
        audio_only = False
        if download_type.get() == "playlist":
            audio_only = messagebox.askyesno(
                "Choose format",
                "Download audio-only? (No = video)"
            )

        prog_bar.configure(maximum=100, value=0)

        for item in vids:
            url = tree.item(item, "tags")[0]
            yt = YouTube(url, on_progress_callback=progress_fn)

            # Select stream based on type and playlist/audio setting
            if download_type.get() == "playlist":
                if audio_only:
                    stream = yt.streams.filter(only_audio=True).first()
                    subdir = BASE_DOWNLOAD_DIR / "Playlist" / "Audio"
                else:
                    stream = yt.streams.get_highest_resolution()
                    subdir = BASE_DOWNLOAD_DIR / "Playlist" / "Video"
            else:
                if download_type.get() == "audio":
                    stream = yt.streams.filter(only_audio=True).first()
                    subdir = BASE_DOWNLOAD_DIR / "Audio"
                else:
                    stream = yt.streams.get_highest_resolution()
                    subdir = BASE_DOWNLOAD_DIR / "Video"

            # Ensure the output directory exists
            subdir.mkdir(parents=True, exist_ok=True)

            try:
                stream.download(output_path=str(subdir))
            except Exception as e:
                Messagebox.show_error("Download Error", f"{yt.title}: {e}")

        Messagebox.show_info("Done", f"Downloaded {len(vids)} file(s) to {BASE_DOWNLOAD_DIR}")

    download_btn.configure(command=on_download)

    window.mainloop()


if __name__ == "__main__":
    main()
