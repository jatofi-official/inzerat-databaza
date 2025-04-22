import tkinter as tk
from tkinter import ttk

root = tk.Tk()

title = "Hello World"
title_var = tk.StringVar()
title_var.set(title)  # works

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="Title:").pack(side=tk.LEFT)
title_entry = ttk.Entry(frame, textvariable=title_var, width=40)
title_entry.pack(side=tk.LEFT, padx=5)

# Debug print
print("title_var:", title_var.get())

root.mainloop()
