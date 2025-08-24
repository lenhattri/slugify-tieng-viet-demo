# app.py
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from slugify import slugify_tieng_viet
except Exception:
    try:
        from my_slugify import slugify_tieng_viet
    except Exception as e:
        slugify_tieng_viet = None
        _import_error = e
    else:
        _import_error = None
else:
    _import_error = None


class SlugifyApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.master.title("Slugify Tiếng Việt – Demo UI")
        self.master.geometry("700x320")
        self.master.minsize(560, 240)

        # Biến trạng thái
        self.in_var = tk.StringVar()
        self.out_var = tk.StringVar()
        self.maxlen_var = tk.StringVar()
        self.config_visible = tk.BooleanVar(value=False)

        # Layout
        self.columnconfigure(1, weight=1)
        self.master.bind("<Return>", self._on_enter)

        # Đầu vào
        ttk.Label(self, text="Đầu vào").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.in_entry = ttk.Entry(self, textvariable=self.in_var)
        self.in_entry.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        # Đầu ra
        ttk.Label(self, text="Đầu ra").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.out_entry = ttk.Entry(self, textvariable=self.out_var, state="readonly")
        self.out_entry.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        # Nút config toggle (hàng 2)
        self.config_btn = ttk.Button(self, text="▼ Cấu hình", command=self.toggle_config)
        self.config_btn.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # Khung config (ẩn ban đầu, sẽ hiển thị ở hàng 3)
        self.cfg_frame = ttk.Labelframe(self, text="Cấu hình")
        self.cfg_frame.columnconfigure(1, weight=1)
        ttk.Label(self.cfg_frame, text="max_len").grid(row=0, column=0, sticky="w", padx=(6, 8), pady=6)
        self.maxlen_entry = ttk.Entry(self.cfg_frame, textvariable=self.maxlen_var, width=10)
        self.maxlen_entry.grid(row=0, column=1, sticky="w", pady=6)

        # Nút hành động (hàng 4)
        btns = ttk.Frame(self)
        btns.grid(row=4, column=1, sticky="e", pady=(8, 0))
        self.submit_btn = ttk.Button(btns, text="Submit", command=self.on_submit)
        self.clear_btn = ttk.Button(btns, text="Xóa", command=self.on_clear, state="disabled")
        self.submit_btn.grid(row=0, column=0, padx=(0, 8))
        self.clear_btn.grid(row=0, column=1)

        # Cảnh báo import
        if slugify_tieng_viet is None:
            ttk.Label(
                self,
                foreground="#b00020",
                text="Không import được slugify_tieng_viet. Đặt app.py cùng thư mục với slugify.py hoặc my_slugify.py."
            ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.pack(fill="both", expand=True)
        self.in_entry.focus()

        # Theo dõi để bật/tắt nút Xóa
        self.out_var.trace_add("write", lambda *_: self._update_clear_state())

    def toggle_config(self):
        if self.config_visible.get():
            self.cfg_frame.grid_forget()
            self.config_visible.set(False)
            self.config_btn.config(text="▼ Cấu hình")
        else:
            self.cfg_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(2, 0))
            self.config_visible.set(True)
            self.config_btn.config(text="▲ Cấu hình")

    def _on_enter(self, event):
        self.on_submit()
        return "break"

    def on_submit(self):
        if slugify_tieng_viet is None:
            messagebox.showerror("Lỗi import", f"Không tìm thấy slugify_tieng_viet\nChi tiết: {_import_error}")
            return

        src = self.in_var.get().strip()
        maxlen = self._parse_maxlen()

        out = slugify_tieng_viet(src, max_len=maxlen)
        self.out_entry.configure(state="normal")
        self.out_var.set(out)
        self.out_entry.configure(state="readonly")

    def on_clear(self):
        self.in_var.set("")
        self.out_entry.configure(state="normal")
        self.out_var.set("")
        self.out_entry.configure(state="readonly")
        self.in_entry.focus()
        # Collapse config khi bấm Xóa
        if self.config_visible.get():
            self.toggle_config()

    def _update_clear_state(self):
        self.clear_btn.configure(state="normal" if self.out_var.get() else "disabled")

    def _parse_maxlen(self):
        raw = self.maxlen_var.get().strip()
        if not raw:
            return None
        try:
            val = int(raw)
            if val < 0:
                return None
            return val
        except ValueError:
            messagebox.showwarning("Cấu hình sai", "max_len phải là số nguyên không âm hoặc để trống.")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        for theme in ("xpnative", "vista", "clam"):
            if theme in style.theme_names():
                style.theme_use(theme)
                break
    except Exception:
        pass
    app = SlugifyApp(root)
    root.mainloop()
