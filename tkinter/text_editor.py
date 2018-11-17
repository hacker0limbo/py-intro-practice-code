import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class TextEditor(object):
    """A simple text editing application"""
    def __init__(self, master):
        """A simple text editing application.
        
        Constructor: TextEditor(Tk.BaseWindow)
        
        """
        self._master = master
        master.title("Text Editor")

        self._filename = ''
        self._is_edited = False

        self._text = tk.Text(master)
        self._text.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._text.bind("<Key>", self._set_edited)

        # Create the menu
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Exit", command=self.close)

        helpmenu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about)

        master.protocol("WM_DELETE_WINDOW", self.close)

    def new(self):
        """Create a new file.
        
        texteditor.new() -> None
        
        """
        if self._can_close():
            # Forget about the currently open file.
            self._text.delete(1.0, tk.END)
            self._filename = ''
            self._master.title("Text Editor")
            self._is_edited = False

    def open_file(self):
        """Open a file.
        
        texteditor.open_file() -> None
        
        """
        if not self._can_close():
            return

        self._filename = filedialog.askopenfilename()
        if self._filename:
            f = open(self._filename, "r")
            text = f.read()
            f.close()

            self._text.delete(1.0, tk.END)
            self._text.insert(tk.END, text)
            self._master.title("Text Editor: {0}".format(self._filename))
            self._is_edited = False

    def save(self):
        """Perform the "Save" functionality.
        
        texteditor.save() -> None
        
        """
        if not self._filename:
            self._filename = filedialog.asksaveasfilename()
        self._perform_save()

    def save_as(self):
        """Perform the "Save As..." functionality.
        
        texteditor.save_as() -> None
        
        """
        filename = filedialog.asksaveasfilename()
        if filename:
            self._filename = filename
        self._perform_save()

    def close(self):
        """Exit the application.
        
        texteditor.close() -> None
        
        """
        if self._can_close():
            self._master.destroy()

    def about(self):
        """Generate an 'About' dialog.
        
        texteditor.about() -> None
        
        """
        messagebox.showinfo(title="Text Editor", message="A simple text editor")

    def _set_edited(self, event):
        """Record that the text file has been edited.
        
        texteditor._set_edited(Tk.Event) -> None
        
        """
        self._is_edited = True

    def _perform_save(self):
        """The functionality behind "Save" and "Save As...".
        
        texteditor._perform_save() -> None
        
        """
        if self._filename:
            self._master.title("Text Editor: {0}".format(self._filename))
            f = open(self._filename, "w")
            text = self._text.get(1.0, tk.END)[:-1]
            f.write(text)
            f.close()
            self._is_edited = False

    def _can_close(self):
        """Check if the file needs to be saved.

        Return True if it is safe to close this file,
        return False if the user wants to continue editing.

        texteditor._can_close() -> bool

        """
        if self._is_edited:
            reply = messagebox.askquestion(type=messagebox.YESNOCANCEL,
                        title="File not saved!",
                        message="Would you like to save this file?")
            if reply == messagebox.YES:
                self.save()
                return True
            elif reply == messagebox.NO:
                return True
            elif reply == messagebox.CANCEL:
                return False
        else:
            return True


root = tk.Tk()
TextEditor(root)
root.mainloop()
