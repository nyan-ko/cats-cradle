from tkinter import Tk, ttk, StringVar

root = Tk()

root.title("Cats Cradle")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky="NEWS")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky="NEWS")

ttk.Button(root, text="Hello World").grid()
root.mainloop()
