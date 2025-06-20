import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def build_ui(master):
    style = ttk.Style()

    # Main container
    root = ttk.Frame(master, padding=10)
    root.pack(fill=BOTH, expand=YES)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)

    # Header sections
    header_frame = ttk.Frame(root, padding=(10, 10, 10, 0))
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    header_label = ttk.Label(
        header_frame,
        text="Youtube Downloader",
        font=("Helvetica", 24, "bold")
    )
    header_label.pack(side=LEFT)

    # Theme toggle
    theme = ttk.StringVar(value=style.theme.name)
    def apply_theme():
        style.theme_use(theme.get())

    ttk.Radiobutton(
        header_frame, text="Light", value="cosmo",
        variable=theme, command=apply_theme
    ).pack(side=RIGHT)
    ttk.Radiobutton(
        header_frame, text="Dark", value="superhero",
        variable=theme, command=apply_theme
    ).pack(side=RIGHT, padx=5)

    ttk.Separator(root).grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

    # video,audio,playlist options
    options_frame = ttk.Labelframe(
        root, text="Download type", padding=10)
    options_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
    download_type = ttk.StringVar(value="audio")
    for text, val in [("Audio","audio"),("Video","video"),("Playlist","playlist")]:
        ttk.Radiobutton(
            options_frame, text=text, variable=download_type, value=val
        ).pack(side=LEFT, expand=YES, padx=5)

    # left panel with entry, thumbnail, and centered btns
    lpanel = ttk.Frame(root, padding=5)
    lpanel.grid(row=3, column=0, sticky="nsew", padx=(0,10))
    lpanel.columnconfigure(0, weight=1)

    center_container = ttk.Frame(lpanel)
    center_container.pack(fill=X, pady=20)

    thumb_container = ttk.Frame(center_container, width=320, height=180)
    thumb_container.pack()
    thumb_container.pack_propagate(False)
    video_label = ttk.Label(thumb_container)
    video_label.pack(fill=BOTH, expand=YES)

    url_frame = ttk.Frame(center_container)
    url_frame.pack(pady=(15,0))
    url_entry = ttk.Entry(url_frame, width=80)
    url_entry.pack(side=LEFT)
    clear_btn = ttk.Button(
        url_frame,
        text="Clear",
        width=6,
        command=lambda: url_entry.delete(0, END)
    )
    clear_btn.pack(side=LEFT, padx=(5,0))

    btn_frame = ttk.Frame(center_container)
    btn_frame.pack(pady=(10,0))
    submit_btn = ttk.Button(
        btn_frame, text="Submit", bootstyle="primary", width=12
    )
    download_btn = ttk.Button(
        btn_frame, text="Download", bootstyle="success", width=12
    )
    submit_btn.pack(side=LEFT, padx=8)
    download_btn.pack(side=LEFT, padx=8)

    # right frame and treeview with hree columns: ID, Video Name, and Duration
    rpanel = ttk.Frame(root, padding=5)
    rpanel.grid(row=3, column=1, sticky="nsew")
    rpanel.columnconfigure(0, weight=1)
    rpanel.rowconfigure(0, weight=1)

    loaded_tree = ttk.Treeview(
        rpanel,
        columns=("id", "name", "duration"),
        show="headings",
        height=15
    )
    loaded_tree = ttk.Treeview(master=rpanel, columns=[0, 1, 2], show="headings", height=10)
    loaded_tree.heading(0, text="No.")
    loaded_tree.heading(1, text="Video Name")
    loaded_tree.heading(2, text="Duration")
    loaded_tree.column(0, width=50, anchor="w")
    loaded_tree.column(1, width=200, anchor=W)
    loaded_tree.column(2, width=100, anchor=SE)
    
    loaded_tree.pack(fill=Y, expand=YES, anchor="se")

    return {
        "root": root,
        "theme": theme,
        "download_type": download_type,
        "url_entry": url_entry,
        "clear_btn": clear_btn,
        "submit_btn": submit_btn,
        "download_btn": download_btn,
        "loaded_tree": loaded_tree,
        "video_label": video_label
    }
