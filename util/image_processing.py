import cv2
import numpy as np
from tkinter import PhotoImage


def threshold_image(image, start, end, tolerance, extra_probes):
    color_start = int(image[start])
    color_end = int(image[end])
    print(f'start col: {color_start}, end col: {color_end}')
    mean_color = (color_start + color_end) / 2

    # sprawdzanie czy zakresy sie zgadzaja
    lower = mean_color - mean_color * tolerance
    lower = lower if 0 <= lower <= 255 else 0
    lower = int(lower)

    upper = mean_color + mean_color * tolerance
    upper = upper if 0 <= upper <= 255 else 255
    upper = int(upper)

    print(f'lower thresh: {lower}, upper thresh: {upper}')

    ret = cv2.inRange(image, lower, upper)

    for probe in extra_probes:
        probe_color = int(image[probe])
        lower_probe = probe_color - probe_color * tolerance
        lower_probe = lower_probe if 0 <= lower_probe <= 255 else 0
        lower_probe = int(lower_probe)

        upper_probe = probe_color + probe_color * tolerance
        upper_probe = upper_probe if 0 <= upper_probe <= 255 else 255
        upper_probe = int(upper_probe)

        probed_image = cv2.inRange(image, lower_probe, upper_probe)

        ret = cv2.bitwise_or(ret, probed_image)

    return ret


def averaging_filter_road_weight(image, filter_size=5, minimum_pixel_weight=10):
    kernel = np.ones((filter_size, filter_size), np.float32) / filter_size**2

    # filtr uśredniający
    filtered_image = cv2.filter2D(image, -1, kernel)
    # nowe wagi bierzemy tylko tam gdzie w oryginale w środku filtra nie było zero
    ret_image = cv2.bitwise_and(filtered_image, filtered_image, mask=image)
    # odwracanie kolorów jeśli potrzeba (jeśli potrzeba XDDD, pewnie że trzeba - dopisek późniejszy)
    ret_image = ~ret_image
    # każdy piksel powinien mieć minium wartość bo algorytm Dijkstry może zacząć robić "pętle"
    ret_image[ret_image < minimum_pixel_weight] = minimum_pixel_weight

    return ret_image


def array_to_photo_image(image: np.ndarray):
    height, width = image.shape[:2]
    ppm_header = f'P6 {width} {height} 255 '.encode()
    data = ppm_header + cv2.cvtColor(image, cv2.COLOR_BGR2RGB).tobytes()
    return PhotoImage(width=width, height=height, data=data, format='PPM')
