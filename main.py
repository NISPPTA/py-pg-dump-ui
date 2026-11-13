# O arquivo que você de fato executa. Limpo e focado apenas em disparar o loop do sistema.

import tkinter as tk

from gui.main_window import MainWindow


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
