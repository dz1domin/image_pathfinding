# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from tkinter import ttk, filedialog
from tkinter import *
from PIL import Image, ImageTk
import cv2


class application:

    def __init__(self):
        self.tk = Tk()
        self.piv = 0
        self.result = []
        self.width = 0
        self.file_path = ""
        self.state = True
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.tk.attributes("-fullscreen", False)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.configure(background='#F0F8FF')
        self.tk.title('IMAGE ANALYSIS PROJECT')

        Button(self.tk, text='Upload Photo', bg='#F0F8FF', font=("Times New Roman", 12, 'normal'),
               command=self.loadPicture).place(x=62, y=38)

        Button(self.tk, text='Find Path', bg='#F0F8FF', font=("Times New Roman", 12, 'normal'),
               command=self.findpath).place(x=66, y=80)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def changeImage(self, img):
        self.picture.create_image(1000, 0, anchor=NE, image=img)
        mainloop()

    def loadPicture(self):
        self.piv = 0
        self.file_path = filedialog.askopenfilename()
        try:
            print(self.file_path)

            novi = Toplevel()
            canvas = Canvas(novi, width=300, height=200)
            canvas.pack(expand=YES, fill=BOTH)
            gif1 = PhotoImage(file=self.file_path)

            canvas.create_image(0, 0, image=gif1, anchor=NW)

            canvas.gif1 = gif1
            novi.canva = canvas
            novi.bind('<Button-1>', self.getxy)
        except:
            print(self.file_path)
            print("wrong file path")

    def getxy(self, event):
        print("Position = ({0},{1})".format(event.x, event.y))
        if self.x1 == 0 and self.y1 == 0:
            self.x1 = event.x
            self.y1 = event.y
            print("Starting Position = ({0},{1})".format(self.x1, self.y1))
        else:
            self.x2 = event.x
            self.y2 = event.y
            print("Ending Position = ({0},{1})".format(self.x2, self.y2))

    def changeImage2(self, img):
        self.picture.create_image(1000, 0, anchor=NE, image=img)
        mainloop()
    def findpath(self):
        print("logika")
        # novi2 = Toplevel()
        # canvas = Canvas(novi2, width=300, height=200)
        # canvas.pack(expand=YES, fill=BOTH)
        # gif2 = PhotoImage(file=self.file_path)
        #
        # canvas.create_image(0, 0, image=gif2, anchor=NW)
        #
        # canvas.gif1 = gif2
        # novi2.canva = canvas

if __name__ == '__main__':
    w = application()
    w.tk.mainloop()
