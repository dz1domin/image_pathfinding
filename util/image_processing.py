import cv2
import numpy as np


def threshold_image(image, start, end, tolerance):
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

    return cv2.inRange(image, lower, upper)


def averaging_filter_road_weight(image, filter_size=5):
    kernel = np.ones((filter_size, filter_size), np.float32) / filter_size**2

    # filtr uśredniający
    filtered_image = cv2.filter2D(image, -1, kernel)
    # nowe wagi bierzemy tylko tam gdzie w oryginale w środku filtra nie było zero
    ret_image = cv2.bitwise_and(filtered_image, filtered_image, mask=image)

    return ret_image
