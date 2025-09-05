import tkinter as tk
from ui import MainApp


def main():
    root = tk.Tk()
    root.geometry("450x600")
    app = MainApp(root)
    root.resizable(False, False)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()
