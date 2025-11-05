"""
message_helper.py
Safe helper for manual sending to desktop WhatsApp.
Load a list of messages (one per line) or auto-generate.
Click "Copy Next" to copy the next message to clipboard.
Then switch to WhatsApp group and press Ctrl+V, Enter to send manually.

Requires: pip install pyperclip
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyperclip
import os

MAX_MESSAGES = 100

class MessageHelper:
    def __init__(self, root):
        self.root = root
        root.title("Safe WhatsApp Message Helper")
        root.geometry("600x420")
        self.messages = []
        self.index = 0

        # UI
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill="x")

        tk.Button(top_frame, text="Load from file", command=self.load_file).pack(side="left", padx=6)
        tk.Button(top_frame, text="Paste messages", command=self.paste_messages).pack(side="left", padx=6)
        tk.Button(top_frame, text="Generate sample 100", command=self.generate_sample).pack(side="left", padx=6)

        mid = tk.Frame(root)
        mid.pack(fill="both", expand=True, padx=10, pady=8)

        self.txt = tk.Text(mid, wrap="word")
        self.txt.pack(fill="both", expand=True)

        bottom = tk.Frame(root, pady=8)
        bottom.pack(fill="x")

        self.status_var = tk.StringVar()
        self.update_status()

        tk.Button(bottom, text="Copy Next →", command=self.copy_next, width=12).pack(side="left", padx=6)
        tk.Button(bottom, text="Copy Prev ←", command=self.copy_prev, width=12).pack(side="left", padx=6)
        tk.Button(bottom, text="Reset", command=self.reset_list, width=8).pack(side="left", padx=6)
        tk.Button(bottom, text="Open folder", command=self.open_folder, width=10).pack(side="left", padx=6)

        tk.Label(bottom, textvariable=self.status_var).pack(side="right", padx=8)

        # initial message explaining usage
        intro = (
            "Usage:\n"
            "1. Load a text file where each line is a message (or click Generate sample).\n"
            "2. Select 'Copy Next' to copy the next message to clipboard.\n"
            "3. Switch to WhatsApp Desktop window, paste (Ctrl+V) and press Enter to send.\n\n"
            "This app DOES NOT send messages automatically — you send them manually to stay within rules."
        )
        self.txt.insert("1.0", intro)

    def update_status(self):
        self.status_var.set(f"Message {self.index}/{len(self.messages)} (max {MAX_MESSAGES})")

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Select messages file (one message per line)",
            filetypes=[("Text files","*.txt"),("All files","*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\n") for line in f]
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return
        # flatten and filter empty lines, limit to MAX_MESSAGES
        msgs = [ln for ln in lines if ln.strip()]
        if len(msgs) > MAX_MESSAGES:
            if not messagebox.askyesno("Too many messages",
                                       f"File contains {len(msgs)} messages. Only first {MAX_MESSAGES} will be used. Continue?"):
                return
            msgs = msgs[:MAX_MESSAGES]
        self.messages = msgs
        self.index = 0
        self.refresh_text_area()
        self.update_status()

    def paste_messages(self):
        # get clipboard, paste as many lines as present
        content = pyperclip.paste()
        if not content.strip():
            messagebox.showinfo("No text", "Clipboard is empty.")
            return
        lines = [ln for ln in content.splitlines() if ln.strip()]
        if not lines:
            messagebox.showinfo("No messages", "No non-empty lines found in clipboard.")
            return
        if len(lines) > MAX_MESSAGES:
            if not messagebox.askyesno("Too many messages",
                                       f"Clipboard contains {len(lines)} messages. Only first {MAX_MESSAGES} will be used. Continue?"):
                return
            lines = lines[:MAX_MESSAGES]
        self.messages = lines
        self.index = 0
        self.refresh_text_area()
        self.update_status()

    def generate_sample(self):
        count = simpledialog.askinteger("How many?", "Number of sample messages (max 100):", initialvalue=20, minvalue=1, maxvalue=MAX_MESSAGES)
        if not count:
            return
        self.messages = [f"Hello — sample message #{i+1} 😊" for i in range(count)]
        self.index = 0
        self.refresh_text_area()
        self.update_status()

    def refresh_text_area(self):
        self.txt.delete("1.0", "end")
        header = f"Loaded {len(self.messages)} messages. Click 'Copy Next' to copy message to clipboard.\n\n"
        self.txt.insert("1.0", header)
        for i, m in enumerate(self.messages, start=1):
            mark = "→" if i-1 == self.index else "  "
            self.txt.insert("end", f"{mark} [{i}] {m}\n\n")

    def copy_next(self):
        if not self.messages:
            messagebox.showinfo("No messages", "Load or generate messages first.")
            return
        if self.index >= len(self.messages):
            messagebox.showinfo("Done", "You reached the end of the message list.")
            return
        msg = self.messages[self.index]
        pyperclip.copy(msg)
        self.index += 1
        self.update_status()
        self.refresh_text_area()
        # small visual confirmation
        self.root.after(100, lambda: self.root.focus_force())

    def copy_prev(self):
        if not self.messages:
            return
        if self.index <= 1:
            self.index = 0
        else:
            self.index -= 1
        if self.index < len(self.messages):
            pyperclip.copy(self.messages[self.index])
        self.update_status()
        self.refresh_text_area()

    def reset_list(self):
        if not self.messages:
            return
        if messagebox.askyesno("Reset", "Clear all loaded messages?"):
            self.messages = []
            self.index = 0
            self.txt.delete("1.0", "end")
            self.txt.insert("1.0", "No messages loaded. Use 'Load from file' or 'Generate sample 100'.")
            self.update_status()

    def open_folder(self):
        # opens current directory in file explorer (convenience)
        try:
            path = os.getcwd()
            if os.name == "nt":
                os.startfile(path)
            elif os.name == "posix":
                os.system(f'xdg-open "{path}"')
            else:
                messagebox.showinfo("Open folder", f"Open folder not supported on this OS.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageHelper(root)
    root.mainloop()
