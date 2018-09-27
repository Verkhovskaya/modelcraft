import numpy as np
import os
from fpdf import FPDF
from PIL import Image
import shutil
import sys
import copy
import random


def draw_level(pixel_size, color_array):
    colors = {0: [255, 255, 255], 1: [0,0,0]}
    pixel_size = pixel_size/3
    down = max(color_array.shape[0], color_array.shape[1])
    across = min(color_array.shape[0], color_array.shape[1])
    image = np.zeros(((down+1) * pixel_size, (across + 1) * pixel_size, 3), dtype=np.uint8) + 100
    for x in range(color_array.shape[0]):
        for y in range(color_array.shape[1]):
            if color_array.shape[1] > color_array.shape[0]:
                down, across = y,x
            else:
                down, across = x,y
            image[down * pixel_size + 5:(down + 1) * pixel_size + 5, across * pixel_size + 5:(across + 1) * pixel_size + 5] = colors[int(color_array[x, y])]
    return image


def generate_layout_files(root_path, session_id, block_array, type=["pdf"]):
    image_paths = generate_layout_images(root_path, session_id, block_array)
    generate_layout_pdf(root_path, session_id, image_paths)


def generate_layout_images(root_path, session_id, block_array):
    folder_path = root_path + "/data/" + session_id + "/layout_images"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)

    not_zero = lambda x: x != 0
    color_array = 1*not_zero(block_array)
    image_names = []
    for z in range(color_array.shape[2]):
        data = draw_level(10, color_array[:, :, z])
        img = Image.fromarray(data, 'RGB')
        img_name = folder_path + "/" + str(z) + ".png"
        image_names.append(img_name)
        img.save(img_name)

    return image_names


def generate_layout_pdf(root_path, session_id, image_paths):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(root_path + "/graphics/front_page.jpeg", 5, 0, 200, 275)
    # imagelist is the list with all image filenames
    for image in image_paths:
        pdf.add_page()
        pdf.image(image, 5, 5, 200, 250)
    pdf.output(root_path + "/data/" + session_id + "/layout.pdf", "F")
