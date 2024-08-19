import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os
import threading
import sys
import io

class StdoutRedirector(io.TextIOBase):
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.configure(state='normal')

    def write(self, s):
        self.text_widget.insert(tk.END, s)
        self.text_widget.see(tk.END)  # Автопрокрутка до конца текста
        self.text_widget.update_idletasks()

    def flush(self):
        pass

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("AVI files", "*.avi;*.AVI")])
    if file_path:
        file_path_var.set(file_path)
        log_text.insert(tk.END, f"Selected file: {file_path}\n")

def convert_video():
    avi_file_path = file_path_var.get()

    if not avi_file_path:
        messagebox.showerror("Error", "No file selected. Please select a file first.")
        return

    try:
        log_text.insert(tk.END, "Starting conversion...\n")

        video_clip = VideoFileClip(avi_file_path)

        if remove_sound_var.get():
            video_clip = video_clip.without_audio()
            log_text.insert(tk.END, "Audio track removed.\n")

        current_directory = os.getcwd()
        output_file = os.path.join(current_directory, os.path.basename(avi_file_path).replace(".avi", ".mp4").replace(".AVI", ".mp4"))

        log_text.insert(tk.END, f"Output file path: {output_file}\n")

        # Выполнение конвертации и отображение прогресса
        video_clip.write_videofile(output_file, codec="libx264")

        log_text.insert(tk.END, "Conversion completed successfully!\n")
        messagebox.showinfo("Success", f"Video converted successfully!\nSaved as: {output_file}")

    except Exception as e:
        log_text.insert(tk.END, f"An error occurred: {str(e)}\n")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        log_text.insert(tk.END, "Process finished.\n")

def start_conversion_thread():
    thread = threading.Thread(target=convert_video)
    thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("AVI to MP4 Converter with Remove Sound Option")
    root.geometry("600x400")

    file_path_var = tk.StringVar()

    select_file_button = tk.Button(root, text="Select AVI File", command=select_file)
    select_file_button.pack(pady=10)

    remove_sound_var = tk.BooleanVar()

    remove_sound_checkbox = tk.Checkbutton(root, text="Remove Sound", variable=remove_sound_var)
    remove_sound_checkbox.pack(pady=10)

    convert_button = tk.Button(root, text="Convert to MP4", command=start_conversion_thread)
    convert_button.pack(pady=10)

    # Добавляем текстовое поле для вывода логов
    log_text = tk.Text(root, wrap='word', height=15)
    log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Перенаправляем stdout в текстовое поле
    sys.stdout = StdoutRedirector(log_text)

    root.mainloop()
