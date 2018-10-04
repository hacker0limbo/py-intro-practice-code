"""
Simple GUI programming exercise to demonstrate component layout
and event handling.
"""

__copyright__ = "Stephen"


import tkinter as tk
from tkinter import messagebox


class Controls(tk.Frame):
    def __init__(self, master, target_widget):
        super().__init__(master)
        self._target_widget = target_widget
        self._colors = {
            'green': 'green',
            'blue': 'blue',
        }
        btn1 = tk.Button(self, text="Change to Green")
        btn1.pack(side=tk.LEFT, pady=10)
        btn1.bind("<Button-1>", self.change_green)

        btn2 = tk.Button(self, text="Change to Blue")
        btn2.pack(side=tk.LEFT, pady=10)
        btn2.bind("<Button-1>", self.change_blue)
    
    """
    抽出 change_colour 和 change_text, 对所有 button 适用
    方法:
        定义一个新的基类(继承自 frame), 让 Controls 和 InputCommand 继承这个类
    """

    def change_colour(self, bg_colour):
        self._target_widget.config(bg=bg_colour)

    def change_text(self, content):
        base_content = f'The table is {content}' 
        self._target_widget.config(text=base_content)

    def change_green(self, event):
        # target = event.widget
        bg_colour = self._colors['green']
        self.change_colour(bg_colour)
        self.change_text(bg_colour)

    def change_blue(self, event):
        # target = event.widget
        bg_colour = self._colors['blue']
        self.change_colour(bg_colour)
        self.change_text(bg_colour)


class InputCommand(tk.Frame):
    def __init__(self, master, target_widget):
        super().__init__(master)
        self._target_widget = target_widget

        label = tk.Label(self, text='Change the colour to: ')
        label.pack(side=tk.LEFT)

        self._entry = tk.Entry(self, width=20)
        self._entry.pack(side=tk.LEFT) 

        btn3 = tk.Button(self, text="Change it!")
        btn3.pack(side=tk.LEFT)
        btn3.bind("<Button-1>", self.modify)

    def change_colour(self, bg_colour):
        self._target_widget.config(bg=bg_colour)

    def change_text(self, content):
        base_content = f'The table is {content}' 
        self._target_widget.config(text=base_content)

    def modify(self, event):
        input_colour = self._entry.get()
        try:
            self.change_colour(input_colour)
            self.change_text(input_colour)
        except tk.TclError:
            messagebox.showerror('Invalid Colour', f'{input_colour} is not a colour')


"""
下面这种写法将 screen 写成了一个类, 里面的属性 _lbl 是一个部件,  因此要通过 screen._lbl 来访问
另外, 如果是普通的在 init 里面声明一个组件, 如上面的 Controls, 那么只是在初始化就有了, 无法进行外部访问进行改变
"""
# class Screen():
#     def __init__(self, master):
#         self._master = master
#         self._lbl = tk.Label(self._master, text="The table is")
#         self._lbl.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


class SampleApp:
    def __init__(self, master):
        master.title("Hello!")
        master.minsize(430, 200)

        screen = tk.Label(master, text="The table is blue", bg='blue')
        screen.pack(side=tk.TOP, expand=True)

        controls = Controls(master, screen)
        controls.pack(side=tk.TOP)
        controls.config(highlightbackground="green", highlightcolor="green", highlightthickness=5)

        inputCommand = InputCommand(master, screen)
        inputCommand.pack(side=tk.TOP)
        inputCommand.config(pady=10)


if __name__ == "__main__" :
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()
