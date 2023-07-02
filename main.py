import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from util.dijkstra import find_fastest_path, paint_fastest_path
from util.image_processing import threshold_image, averaging_filter_road_weight, array_to_photo_image
import cv2
import numpy as np


MAX_IMAGE_HEIGHT = 900
MAX_IMAGE_WIDTH = 1280


class application:

    def __init__(self):
        self.extra_probes = []
        self.novi = None
        self.end_image = None
        self.image_on_canvas = None
        self.canvas = None
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
        self.file_path = filedialog.askopenfilename(filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg *.jpeg'), ('All', '*.*')])
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        if self.file_path == '':
            return

        try:
            # print(self.file_path)
            if self.novi is not None:
                self.novi.destroy()

            self.novi = Toplevel()
            self.im = Image.open(self.file_path)
            self.im = self.im.convert('RGB')
            width, height = self.im.size

            width = width if width < MAX_IMAGE_WIDTH else MAX_IMAGE_WIDTH
            height = height if height < MAX_IMAGE_HEIGHT else MAX_IMAGE_HEIGHT
            pos_x, pos_y = (0, 0)

            self.im = self.im.resize((width, height), Image.LANCZOS)

            self.novi.resizable(False, False)
            self.novi.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
            self.canvas = Canvas(self.novi)
            self.canvas.pack(expand=YES, fill=BOTH)
            gif1 = ImageTk.PhotoImage(self.im)

            self.image_on_canvas = self.canvas.create_image(0, 0, image=gif1, anchor=NW)

            self.canvas.gif1 = gif1
            self.novi.canva = self.canvas
            self.novi.bind('<Button-1>', self.get_xy)
            self.novi.bind('<Button-3>', self.reset_xy)

            self.canva = self.canvas
        except:
            print(self.file_path)
            print("wrong file path")

    def get_xy(self, event):
        print("Position = ({0},{1})".format(event.x, event.y))
        if self.x1 == 0 and self.y1 == 0:
            self.x1 = event.x
            self.y1 = event.y
            self.canva.create_oval(self.x1 - 5, self.y1 - 5, self.x1 + 5, self.y1 + 5, fill="#2fff00", tags=('point'))
        elif self.x2 == 0 and self.y2 == 0:
            self.x2 = event.x
            self.y2 = event.y
            self.canva.create_oval(self.x2 - 5, self.y2 - 5, self.x2 + 5, self.y2 + 5, fill="#ff0000", tags=('point'))
        else:
            self.extra_probes.append((event.y, event.x))
            self.canva.create_oval(self.extra_probes[-1][1] - 5, self.extra_probes[-1][0] - 5,
                                   self.extra_probes[-1][1] + 5, self.extra_probes[-1][0] + 5, fill="#8994b0", tags=('point'))

    def reset_xy(self, event):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.extra_probes = []
        self.canva.delete('point')
        print("Position has been cleared")

    def find_path(self):
        start = (self.y1, self.x1)
        end = (self.y2, self.x2)

        # wyświetlanie każdego kroku przy pomocy cv2 imshow dla debugu głównie
        image = np.asarray(self.im)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # threshold
        thresh_image = threshold_image(gray_image, start, end, float(self.usError.get()), self.extra_probes)
        # cv2.imshow('thresh_image', thresh_image)

        # filter
        filtered_image = averaging_filter_road_weight(thresh_image, int(self.filterSize.get()))
        # cv2.imshow('filtered_image', filtered_image)

        # Dijkstra
        filtered_image = np.asarray(filtered_image, np.uint32)
        filtered_image = filtered_image ** 3
        filtered_image[:, [0, -1]] = filtered_image[[0, -1]] = np.iinfo(filtered_image.dtype).max
        cost, path = find_fastest_path(filtered_image, start, end)
        end_image = paint_fastest_path(image, path)
        # cv2.imshow('end_image', end_image)
        print(f'path cost: {cost}')

        self.end_image = array_to_photo_image(end_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.end_image)

        messagebox.showinfo('Message', f'Path cost: {cost}, average cost per pixel: {(cost / len(path)):.4f}')


if __name__ == '__main__':
    w = application()
    w.tk.mainloop()
