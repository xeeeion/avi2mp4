import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip

root = tk.Tk()
root.title("AVI to MP4 Converter with Remove Sound Option")

file_path_var = tk.StringVar()


def select_file ():
    file_path = filedialog.askopenfilename(filetypes=[("AVI files", "*.avi;*.AVI")])
    if file_path:
        file_path_var.set(file_path)
        # messagebox.showinfo("File Selected", f"Selected file: {file_path}")


def convert_video ():
    avi_file_path = file_path_var.get()

    if not avi_file_path:
        messagebox.showerror("Error", "No file selected. Please select a file first.")
        return

    try:
        video_clip = VideoFileClip(avi_file_path)

        if remove_sound_var.get():
            video_clip = video_clip.without_audio()

        output_file = avi_file_path.replace(".avi", ".mp4").replace(".AVI", ".mp4")

        video_clip.write_videofile(output_file, codec="libx264")
        messagebox.showinfo("Success", f"Video converted successfully!\nSaved as: {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


select_file_button = tk.Button(root, text="Select AVI File", command=select_file)
select_file_button.pack(pady=10)

remove_sound_var = tk.BooleanVar()

remove_sound_checkbox = tk.Checkbutton(root, text="Remove Sound", variable=remove_sound_var)
remove_sound_checkbox.pack(pady=10)

convert_button = tk.Button(root, text="Convert to MP4", command=convert_video)
convert_button.pack(pady=10)

root.mainloop()
