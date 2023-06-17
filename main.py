import tkinter
from tkinter import filedialog
from tkinter import *
from PIL import Image
from util.dijkstra import find_fastest_path, paint_fastest_path, create_graph_from_image
from util.image_processing import threshold_image, averaging_filter_road_weight
import cv2
import numpy as np


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
        self.im = None

        self.tk.attributes("-fullscreen", False)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.configure(background='#F0F8FF')
        self.tk.title('AiPO')

        self.canva = None

        Button(self.tk, text='Load Photo', bg='#F0F8FF', font=("Times New Roman", 12, 'normal'),
               command=self.load_picture).place(x=62, y=38)

        Button(self.tk, text='Find Path', bg='#F0F8FF', font=("Times New Roman", 12, 'normal'),
               command=self.find_path).place(x=76, y=80)

        text1 = Label(self.tk, text='Custom Error')
        text1.place(x=52, y=150)

        self.usError = Entry(self.tk)
        self.usError.place(x=52, y=176)
        # defualt wartość błędu
        self.usError.insert(tkinter.END, '0.05')

        text2 = Label(self.tk, text='Filter Size')
        text2.place(x=52, y=230)
        self.filterSize = Entry(self.tk)
        self.filterSize.place(x=52, y=250)
        # defualt wartość filtru
        self.filterSize.insert(tkinter.END, '5')

        self.tk.resizable(False, False)
        self.tk.geometry("230x310")

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def load_picture(self):
        self.piv = 0
        self.file_path = filedialog.askopenfilename()
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        try:
            print(self.file_path)

            novi = Toplevel()
            self.im = Image.open(self.file_path)
            width, height = self.im.size
            novi.resizable(False, False)
            novi.geometry(str(width) + "x" + str(height))
            canvas = Canvas(novi, width=300, height=200)
            canvas.pack(expand=YES, fill=BOTH)
            gif1 = PhotoImage(file=self.file_path)

            canvas.create_image(0, 0, image=gif1, anchor=NW)

            canvas.gif1 = gif1
            novi.canva = canvas
            novi.bind('<Button-1>', self.get_xy)

            self.canva = canvas
        except:
            print(self.file_path)
            print("wrong file path")

    def get_xy(self, event):
        print("Position = ({0},{1})".format(event.x, event.y))
        if self.x1 == 0 and self.y1 == 0:
            self.x1 = event.x
            self.y1 = event.y
            self.canva.create_oval(self.x1 - 5, self.y1 - 5, self.x1 + 5, self.y1 + 5, fill="#2fff00")
            print("Starting Position = ({0},{1})".format(self.x1, self.y1))
        else:
            self.x2 = event.x
            self.y2 = event.y
            self.canva.create_oval(self.x2 - 5, self.y2 - 5, self.x2 + 5, self.y2 + 5, fill="#ff0000")
            print("Ending Position = ({0},{1})".format(self.x2, self.y2))

    def find_path(self):
        start = (self.y1, self.x1)
        end = (self.y2, self.x2)

        # wyświetlanie każdego kroku przy pomocy cv2 imshow dla debugu głównie
        image = np.asarray(self.im)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray_image', gray_image)

        # threshold
        thresh_image = threshold_image(gray_image, start, end, float(self.usError.get()))
        cv2.imshow('thresh_image', thresh_image)

        # filter
        filtered_image = averaging_filter_road_weight(thresh_image, int(self.filterSize.get()))
        # odwracanie kolorów jeśli potrzeba
        filtered_image = ~filtered_image
        cv2.imshow('filtered_image', filtered_image)

        # Dijkstra
        graph = create_graph_from_image(filtered_image)
        cost, path = find_fastest_path(graph, start, end)
        end_image = paint_fastest_path(image, path)
        cv2.imshow('end_image', end_image)

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
