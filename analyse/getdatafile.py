# DEPRECATED #
from tkinter import filedialog
from tkinter import *

raise DeprecationWarning('This file is no longer in use')

def getpath():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="databin/", title="Select file",
                                               filetypes=(("csv Flight Data", "*.csv"), ("all files", "*.*")))
    return root.filename
