"""
Simple GUI programming exercise to demonstrate component layout
and event handling.
"""

__copyright__ = "Stephen"

"""
总结思考:
    1, Controls 和 InputCommand 都继承自 tk.Frame, 同时又都有相同的 change_colour() 和 change_text() 方法
        可以考虑抽出形成一个新类, 这个新基类继承 tk.Frame, Controls 和 InputCommand 继承这个心类
    2, 一个类里面如果使用 self.xxx 来声明一个部件, 说明这个部件是这个类的一部分(属性), 可以访问并且修改这个部件的配置
        如果单纯的在 __init__() 里面声明部件, 初始化以后就无法修改. 
"""

import tkinter as tk
from tkinter import messagebox

class Trigger(tk.Frame):
    def __init__(self, master, target_widget):
        super().__init__(master)
        self._target_widget = target_widget

    def change_colour(self, bg_colour):
        self._target_widget.config(bg=bg_colour)

    def change_text(self, content):
        base_content = f'The table is {content}' 
        self._target_widget.config(text=base_content)


class Controls(Trigger):
    def __init__(self, master, target_widget):
        super().__init__(master, target_widget)
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
    
    def change_green(self, event):
        bg_colour = self._colors['green']
        self.change_colour(bg_colour)
        self.change_text(bg_colour)

    def change_blue(self, event):
        bg_colour = self._colors['blue']
        self.change_colour(bg_colour)
        self.change_text(bg_colour)


class InputCommand(Trigger):
    def __init__(self, master, target_widget):
        super().__init__(master, target_widget)

        label = tk.Label(self, text='Change the colour to: ')
        label.pack(side=tk.LEFT)

        self._entry = tk.Entry(self, width=20)
        self._entry.pack(side=tk.LEFT) 

        btn3 = tk.Button(self, text="Change it!")
        btn3.pack(side=tk.LEFT)
        btn3.bind("<Button-1>", self.modify)

    def modify(self, event):
        """
        当输入的内容不是有效的 color 时触发 tk.TclError 错误
        """
        input_colour = self._entry.get()
        try:
            self.change_colour(input_colour)
            self.change_text(input_colour)
        except tk.TclError:
            messagebox.showerror('Invalid Colour', f'{input_colour} is not a colour')


class SampleApp:
    def __init__(self, master):
        master.title("Hello!")
        master.minsize(430, 200)

        screen = tk.Label(master, text="The table is blue", bg='blue')
        screen.pack(side=tk.TOP, expand=True)

        controls = Controls(master, screen)
        controls.pack(side=tk.TOP)
        controls.config(highlightbackground="green", highlightcolor="green", highlightthickness=100)

        inputCommand = InputCommand(master, screen)
        inputCommand.pack(side=tk.TOP)
        inputCommand.config(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SampleApp(root)
    root.mainloop()
