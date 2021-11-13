#!/usr/bin/env python3
# ImageProcessorX
# (c) 2021 Poikilos
# license: See license file.
'''
This processes a list of images. The list is basically a "playlist" for
images. The last column in the space-separated columns is considered as
the filename. If that is not a file, more columns to the left will be
appended until a file is found, otherwise the line is skipped.

If the filenames are relative, the current working directory must be the
base path in which the relative paths can be used.
'''

dephelp = "sudo apt-get install python3-pil python3-pil.imagetk"
try:
    import Tkinter as tk
    import ttk
    # Python 2
    dephelp = "sudo apt-get install python-imaging python-pil.imagetk"
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk
    from tkinter import ttk

from PIL import Image

try:
    from PIL import ImageTk  # Place this at the end (to avoid any conflicts/errors)
except ImportError as ex:
    print("{}".format(ex))
    print()
    print("You must install ImageTk such as via:")
    print(dephelp)
    print()
    exit(1)

from decimal import Decimal
import decimal
import locale as lc

session = {}
playerIndex = 0

import os
import sys
import math

checkDotTypes = [
    ".png",
    ".jpg",
    ".bmp",
]

class MainFrame(ttk.Frame):
    ISSUE_DIR = 'Specify a directory.'
    ISSUE_LIST = 'Specify a list file.'

    def __init__(self, parent):
        self.img = None
        self.nameSV = tk.StringVar()
        self.pathSV = tk.StringVar()
        self.mainSV = tk.StringVar()
        self.listSV = tk.StringVar()
        self.statusSV = tk.StringVar()
        ttk.Frame.__init__(self, parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.issues = [
            MainFrame.ISSUE_DIR,
            MainFrame.ISSUE_LIST,
        ]
        row = 0
        wide_width = 30
        ttk.Label(self, textvariable=self.statusSV).grid(column=0, row=row, sticky=tk.E, columnspan=2)
        self.statusSV.set("Specify a Directory. Specify a file list.")
        row += 1
        ttk.Label(self, text="Directory:").grid(column=0, row=row, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.mainSV, state="readonly").grid(column=1, columnspan=3, row=row, sticky=tk.W)
        row += 1
        ttk.Label(self, text="List:").grid(column=0, row=row, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.listSV, state="readonly").grid(column=1, columnspan=3, row=row, sticky=tk.W)
        row += 1
        ttk.Label(self, text="Name:").grid(column=0, row=row, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.nameSV, state="readonly").grid(column=1, columnspan=3, row=row, sticky=tk.W)
        row += 1
        ttk.Label(self, text="Path:").grid(column=0, row=row, sticky=tk.E)
        self.pathEntry = ttk.Entry(self, width=25, textvariable=self.pathSV)
        self.pathEntry.grid(column=1, columnspan=3, row=row, sticky=tk.W)
        row += 1
        self.prevBtn = ttk.Button(self, text="Previous", command=self.prevFile)
        self.prevBtn.grid(column=1, row=row, sticky=tk.E)
        self.nextBtn = ttk.Button(self, text="Next", command=self.nextFile)
        self.nextBtn.grid(column=2, row=row, sticky=tk.W)
        row += 1
        self.markBtn = ttk.Button(self, text="Mark", command=self.markFile)
        self.markBtn.grid(column=1, row=row, sticky=tk.E)
        ttk.Button(self, text="Exit", command=root.destroy).grid(column=2, row=row, sticky=tk.W)
        row += 1
        self.imgLabel = ttk.Label(self, text="...")
        self.imgLabel.grid(column=0, row=row, sticky=tk.E, columnspan=2)
        for child in self.winfo_children():
            child.grid_configure(padx=6, pady=3)
        self.nextBtn['state'] = tk.DISABLED
        self.prevBtn['state'] = tk.DISABLED
        # self.nameSV.set(money(session.getCurrentMoney(playerIndex)))

    def setPath(self, path):
        self.issues.remove(MainFrame.ISSUE_DIR)
        # print("self.issues: {}".format(self.issues))
        statusStr = ""
        space = ""
        for issueStr in self.issues:
            statusStr += space + issueStr
            space = " "
        self.statusSV.set(statusStr)
        self.mainSV.set(path)

    def setList(self, path):
        self.issues.remove(MainFrame.ISSUE_LIST)
        print("self.issues: {}".format(self.issues))
        statusStr = ""
        space = ""
        for issueStr in self.issues:
            statusStr += space + issueStr
            space = " "
        self.statusSV.set(statusStr)
        self.listSV.set(path)


    def showImage(self, path):
        '''
        See Apostolos' Apr 14 '18 at 16:20 answer edited Oct 26 '18 at
        8:40 on <https://stackoverflow.com/a/49833564>
        '''
        self.img = ImageTk.PhotoImage(Image.open(path))
        # self.imgLabel = tk.Label(window, image=self.img).pack()
        self.imgLabel.configure(image=self.img)

    def getBasePath(self):
        result = "."
        tmp = self.mainSV.get().strip()
        if len(tmp) > 0:
            result = tmp
        return result

    def getFullPath(self, rel):
        return os.path.join(self.getBasePath(), rel)

    def loadList(self, path):
        self.names = []
        self.nameI = 0
        with open(path, 'r') as ins:
            for rawL in ins:
                line = rawL.strip()
                parts = line.split(" ")
                cols = 1
                name = line[-1]
                while cols <= len(parts):
                    lastParts = parts[-cols:]
                    tryName = " ".join(lastParts)
                    # print("tryName: \"{}\"".format(tryName))
                    tryPath = self.getFullPath(tryName)
                    if os.path.isfile(tryPath):
                        self.names.append(tryName)
                        break
                    cols += 1
        # print("names: {}".format(self.names))


    def onFormLoaded(self):
        path = self.listSV.get().strip()
        if len(path) < 1:
            return
        self.loadList(path)
        if len(self.names) > 0:
            self.showCurrentImage()
            self.prevBtn['state'] = tk.DISABLED
            if len(self.names) > 1:
                self.nextBtn['state'] = tk.NORMAL

    def prevFile(self):
        self.nameI -= 1
        if self.nameI < 0:
            self.nameI = len(self.names) - 1
        self.showCurrentImage()
        self.updateButtonStates()

    def showCurrentImage(self):
        self.showImage(self.names[self.nameI])

    def updateButtonStates(self):
        if self.nameI + 1 < len(self.names):
            self.nextBtn['state'] = tk.NORMAL
        else:
            self.nextBtn['state'] = tk.DISABLED
        if self.nameI > 0:
            self.prevBtn['state'] = tk.NORMAL
        else:
            self.prevBtn['state'] = tk.DISABLED

    def nextFile(self):
        self.nameI += 1
        if self.nameI >= len(self.names):
            self.nameI = 0
        self.showCurrentImage()
        self.updateButtonStates()

    def markFile(self):
        pass

    def end(self):
        self.nextBtn['state'] = tk.DISABLED
        self.prevBtn['state'] = tk.DISABLED
        self.markBtn['state'] = tk.NORMAL


def main():
    global session
    session = {}

    global root
    root = tk.Tk()
    root.title("ImageProcessorX")
    mainframe = MainFrame(root)
    prevArg = None
    mainDirPath = None
    listPath = None
    for arg in sys.argv:
        if prevArg is None:
            prevArg = arg  # the command that ran this script
            continue
        if mainDirPath is None:
            mainDirPath = arg
            mainframe.setPath(arg)
        elif listPath is None:
            listPath = arg
            mainframe.setList(arg)
        prevArg = arg
    root.after(1, mainframe.onFormLoaded)  # (milliseconds, function)
    root.mainloop()
    '''
    session.stop()
    if session.save():
        print("Save completed.")
    else:
        print("Save failed.")
    '''

if __name__ == "__main__":
    main()
