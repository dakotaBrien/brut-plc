import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import ctypes
import os

directory = None


def choose_dir():
    global directory
    directory = fd.askdirectory(title="Choose Directory", initialdir="/", mustexist=True)
    if directory:
        canvas.itemconfig(dir_text, text=f"Directory: {directory}")
        choose_dir_button.config(text="Change Directory")


def create_list():
    global directory
    pass_dict = {}
    if directory is None:
        canvas.itemconfig(dir_text, text=f"Please choose a directory first.")
    else:
        progress.place(x=56, y=400)
        progress.step()
        canvas.itemconfig(status_text, text="Merging lists...")
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename)) as file:
                    content = file.read()
                    lines = content.splitlines()
                    for line in lines:
                        if line == "":
                            pass
                        else:
                            if line in pass_dict:
                                pass_dict[line] += 1
                            else:
                                pass_dict[line] = 1
        progress.step()
        canvas.itemconfig(status_text, text="Sorting entries...")
        sorted_dict = sorted(pass_dict.items(), key=lambda x: x[1], reverse=True)
        progress.step()
        canvas.itemconfig(status_text, text="Writing to file...")
        n = 1
        file_num_determined = False
        while not file_num_determined:
            if not os.path.exists(f"BrutPasswordLists/BrutPasswordList{n}.txt"):
                file_num_determined = True
                progress.step()
            else:
                n += 1
        if not os.path.exists("BrutPasswordLists"):
            os.mkdir("BrutPasswordLists")
            progress.step()
        with open(f"BrutPasswordLists/BrutPasswordList{n}.txt", "w") as file:
            for key, value in sorted_dict:
                file.write(key + "\n")
        progress.place_forget()
        canvas.itemconfig(dir_text, text="")
        canvas.itemconfig(status_text, text="Finished!")
        choose_dir_button.config(text="Choose Directory")


window = tk.Tk()
window.title("{Brut}")
icon = tk.PhotoImage(file="Brut.png")
window.iconphoto(True, icon)
window.config(width=512, height=612)
window.maxsize(width=512, height=612)
if os.name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

canvas = tk.Canvas(width=512, height=612, bg="gray4", highlightthickness=0)
canvas.create_image(256, 306, image=icon)
canvas.create_text(360, 554, text="{Brut.PLC}", font=("Lucida Console", 26, "bold"))
instructions = ("Welcome to the Brut Password List Compiler! To get started, make sure all of your password.txt "
                "files are located in a single directory. Click the \"Choose Directory\" button below to specify the "
                "location of your files. Once you've done that, click the \"Create List\" button to compile your "
                "lists!")
canvas.create_text(256, 200, text=instructions, font=("Lucida Console", 12, "normal"), fill="white", width=420,
                   justify="center")
dir_text = canvas.create_text(256, 360, text="", font=("Lucida Console", 10, "normal"), fill="white", width=400,
                              justify="center")
status_text = canvas.create_text(256, 520, text="", font=("Lucida Console", 8, "normal"), fill="white",
                                 justify="center")
canvas.place(x=0, y=0)

choose_dir_button = tk.Button(text="Choose Directory", command=choose_dir,
                              bg="gray50", font=("Lucida Console", 10, "normal"),
                              borderwidth=0, highlightbackground="black", width=16)
choose_dir_button.place(x=88, y=450)

create_list_button = tk.Button(text="Create List", command=create_list, bg="gray50",
                               font=("Lucida Console", 10, "normal"), borderwidth=0,
                               highlightbackground="black", width=16)
create_list_button.place(x=270, y=450)

s = ttk.Style()
s.theme_use('clam')
s.configure("gray.Horizontal.TProgressbar", foreground="gray45", background="gray45")
progress = ttk.Progressbar(orient="horizontal", length=400, style="gray.Horizontal.TProgressbar", maximum=5)

window.mainloop()
