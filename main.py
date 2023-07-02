import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import tkinter.colorchooser as colorchooser
from tkinter import Scale, Button
from PIL import Image, ImageTk
from util.dijkstra import find_fastest_path, paint_fastest_path
from util.image_processing import threshold_image, averaging_filter_road_weight, array_to_photo_image
import cv2
import numpy as np

MAX_IMAGE_HEIGHT = 900
MAX_IMAGE_WIDTH = 1280


class Application:

    def __init__(self):
        self.extra_probes = []
        self.novi = None
        self.end_image = None
        self.image_on_canvas = None
        self.canvas = None
        self.path_color = (255, 0, 0)
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
        # Set the background color to light green
        self.tk.configure(background='#BDFCC9')
        self.tk.title('AiPO')

        self.canva = None

        Label(self.tk, text='Max Image Width:', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=0, column=0, padx=10, pady=10)
        self.max_width_scale = Scale(
            self.tk, from_=100, to=MAX_IMAGE_WIDTH, orient='horizontal')
        self.max_width_scale.set(MAX_IMAGE_WIDTH)
        self.max_width_scale.configure(bg='#CADC79')
        self.max_width_scale.grid(row=0, column=1, padx=10, pady=10)

        Label(self.tk, text='Max Image Height:', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=1, column=0, padx=10, pady=10)
        self.max_height_scale = Scale(
            self.tk, from_=100, to=MAX_IMAGE_HEIGHT, orient='horizontal')
        self.max_height_scale.set(MAX_IMAGE_HEIGHT)
        self.max_height_scale.configure(bg='#CADC79')
        self.max_height_scale.grid(row=1, column=1, padx=10, pady=10)

        Button(self.tk, text='Load Photo', bg='#8ABF9E', font=("Arial", 12, 'bold'),  # Set font and background color for the button
               command=self.load_picture).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        Label(self.tk, text='Minimum Pixel Weight:', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=3, column=0, padx=10, pady=10)
        self.min_pixel_weight_entry = Entry(self.tk)
        self.min_pixel_weight_entry.grid(row=3, column=1, padx=10, pady=10)
        self.min_pixel_weight_entry.insert(END, '10')

        Label(self.tk, text='Step Value:', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=4, column=0, padx=10, pady=10)
        self.step_value_entry = Entry(self.tk)
        self.step_value_entry.grid(row=4, column=1, padx=10, pady=10)
        self.step_value_entry.insert(END, '1')

        Button(self.tk, text='Choose Path Color', bg='#8ABF9E', font=("Arial", 12, 'bold'),
               command=self.choose_path_color).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        Button(self.tk, text='Find Path', bg='#8ABF9E', font=("Arial", 12, 'bold'),
               command=self.find_path).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        Label(self.tk, text='Path Width:', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=9, column=0, padx=10, pady=10)
        self.path_width_scale = Scale(
            self.tk, from_=1, to=10, orient='horizontal')
        self.path_width_scale.set(2)  # Set an initial value for the path width
        self.path_width_scale.configure(bg='#CADD84')
        self.path_width_scale.grid(row=9, column=1, padx=10, pady=10)

        Label(self.tk, text='Custom Error', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=7, column=0, padx=10, pady=10)
        self.usError = Entry(self.tk)
        self.usError.grid(row=7, column=1, padx=10, pady=10)
        self.usError.insert(END, '0.05')

        Label(self.tk, text='Filter Size', font=('Verdana', 11, 'bold'), bg='#BDFCC9').grid(
            row=8, column=0, padx=10, pady=10)
        self.filterSize = Entry(self.tk)
        self.filterSize.grid(row=8, column=1, padx=10, pady=10)
        self.filterSize.insert(END, '5')

        self.tk.resizable(False, False)
        self.tk.geometry("360x550")

    def choose_path_color(self):
        color = colorchooser.askcolor(
            title='Choose Path Color', color=self.path_color)
        if color[0] is not None:
            # Update path_color with the chosen color
            self.path_color = color[0]

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
        self.file_path = filedialog.askopenfilename(
            filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg *.jpeg'), ('All', '*.*')])
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

            width = self.max_width_scale.get()
            height = self.max_height_scale.get()
            pos_x, pos_y = (0, 0)

            self.im = self.im.resize((width, height), Image.LANCZOS)

            self.novi.resizable(False, False)
            self.novi.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
            self.canvas = Canvas(self.novi)
            self.canvas.pack(expand=YES, fill=BOTH)
            gif1 = ImageTk.PhotoImage(self.im)

            self.image_on_canvas = self.canvas.create_image(
                0, 0, image=gif1, anchor=NW)

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
            self.canva.create_oval(
                self.x1 - 5, self.y1 - 5, self.x1 + 5, self.y1 + 5, fill="#2fff00", tags=('point'))
        elif self.x2 == 0 and self.y2 == 0:
            self.x2 = event.x
            self.y2 = event.y
            self.canva.create_oval(
                self.x2 - 5, self.y2 - 5, self.x2 + 5, self.y2 + 5, fill="#ff0000", tags=('point'))
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

        path_color = self.path_color

        # Get the path width from the scale widget
        path_width = self.path_width_scale.get()

        try:
            min_pixel_weight = int(self.min_pixel_weight_entry.get())
            step_value = int(self.step_value_entry.get())
        except ValueError:
            messagebox.showerror(
                'Error', 'Invalid input for Minimum Pixel Weight or Step Value.')
            return

        thresh_image = threshold_image(gray_image, start, end, float(
            self.usError.get()), self.extra_probes)

        filtered_image = averaging_filter_road_weight(
            thresh_image, int(self.filterSize.get()), minimum_pixel_weight=min_pixel_weight)

        # Dijkstra
        filtered_image = np.asarray(filtered_image, np.uint32)
        filtered_image = filtered_image ** 3
        filtered_image[:, [0, -1]] = filtered_image[[0, -1]
                                                    ] = np.iinfo(filtered_image.dtype).max
        cost, path = find_fastest_path(filtered_image, start, end)
        # Paint the fastest path with the chosen path color and width
        end_image = paint_fastest_path(
            image, path, color_bgr=path_color, path_width=path_width, skip_step=step_value)
        # cv2.imshow,('end_image', end_image)
        print(f'path cost: {cost}')

        self.end_image = array_to_photo_image(end_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.end_image)

        messagebox.showinfo(
            'Message', f'Path cost: {cost}, average cost per pixel: {(cost / len(path)):.4f}')


if __name__ == '__main__':
    w = Application()
    w.tk.mainloop()
