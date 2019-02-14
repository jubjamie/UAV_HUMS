from tkinter import filedialog
from tkinter import *


def getpath():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="databin/", title="Select file",
                                               filetypes=(("csv Flight Data", "*.csv"), ("all files", "*.*")))
    return root.filename
