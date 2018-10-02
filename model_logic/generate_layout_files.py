import numpy as np
import os
from fpdf import FPDF
from PIL import Image
import shutil
import sys
import copy
import random
from .shared_utils import get_sections, set_render_state
import math


def draw_level(pixel_size, color_array, section_locations):
    colors = {1: [0,0,0], 0: [255, 255, 255]}
    down = color_array.shape[1]
    across = color_array.shape[0]
    image = np.zeros(((down) * pixel_size, (across) * pixel_size, 3), dtype=np.uint8) + 100
    for x in range(color_array.shape[0]):
        for y in range(color_array.shape[1]):
            image[y * pixel_size:(y + 1) * pixel_size, x * pixel_size:(x + 1) * pixel_size] = colors[int(color_array[x, y])]

    if section_locations:
        sections_x = section_locations[1]
        sections_y = section_locations[0]
        for x in sections_x:
            image[max(0,x * pixel_size-2): x*pixel_size+3,:] = [255,0,0]
        for y in sections_y:
            image[:,max(0,y * pixel_size-2): y*pixel_size+3] = [255,0,0]

    for x in range(color_array.shape[1]):
        image[x * pixel_size-1: x*pixel_size+2,:] = [100,100,100]
    for y in range(color_array.shape[0]):
        image[:,y * pixel_size-1: y*pixel_size+2] = [100,100,100]

    return image


def generate_layout_files(root_path, session_id, block_array, section_locations, side_length, type=["pdf"]):
    image_path = root_path + "/data/" + session_id + "/layout_images"
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
    os.mkdir(image_path)

    level_image_paths = generate_level_images(root_path, session_id, image_path, block_array, section_locations)
    generate_level_pdf(root_path, session_id, level_image_paths, side_length, block_array.shape)


def generate_level_images(root_path, session_id, image_path, block_array, section_locations):
    not_zero = lambda x: x != 0
    color_array = 1*not_zero(block_array)
    image_names = []
    for z in range(color_array.shape[2]):
        set_render_state(root_path, session_id, "Drawing layout image " + str(z+1) + " of " + str(color_array.shape[2]),int(20*z/color_array.shape[2]))
        data = draw_level(20, color_array[:, :, z], section_locations)
        img = Image.fromarray(data, 'RGB')
        img_name = image_path + "/" + str(z) + ".png"
        image_names.append(img_name)
        img.save(img_name)

    return image_names


def generate_level_pdf(root_path, session_id, image_paths, side_length, array_shape):
    set_render_state(root_path, session_id, "Generating layout pdf",20)
    page_width = 210  # units
    page_height = 298  # units
    page_margin = 20
    mm = page_width/(8*25.4)  # units
    array_x = array_shape[0]*mm*side_length
    array_y = array_shape[1]*mm*side_length
    text_y = 10

    pdf = FPDF()
    pdf.add_page()
    pdf.image(root_path + "/graphics/front_page.jpeg", 0, 0, 200, 275)
    pdf.set_font('Times', 'B', 20)
    pdf.set_text_color(36,160,226)

    img_x = array_shape[0] * side_length
    img_y = array_shape[1] * side_length

    if img_x < page_width-page_margin*2 and img_y < page_height-page_margin*2:  # 8x11 inches
        while image_paths:
            pdf.add_page()
            num_across = int((page_width-page_margin*2) / img_x)
            num_down = int((page_height-page_margin*2) / (img_y+text_y))
            spacing_x = (page_width-page_margin*2 - num_across * img_x) / (num_across-1)
            spacing_y = (page_height-page_margin*2 - num_down*(text_y+img_y)) / (num_across-1)
            for y in range(num_down):
                for x in range(num_across):
                    if image_paths:
                        image = image_paths.pop(0)
                        level = str(int(image.split("/")[-1][:-4])+1)
                        pdf.text(page_margin+x*spacing_x + x*img_x, page_margin+y*spacing_y-text_y+7 + y*(img_y+text_y), "Level " + level)
                        pdf.image(image, page_margin+x*spacing_x + x*img_x, page_margin+y*spacing_y + y*(img_y+text_y), array_x, array_y)

    else:
        for image in image_paths:
            pages_across = int(math.ceil(img_x/page_width))
            pages_down = int(math.ceil(img_y/page_height))
            for x in range(pages_across):
                for y in range(pages_down):
                    pdf.add_page()
                    pdf.image(image, -x*page_width, -y*page_height, array_x, array_y)
                    pdf.text(page_width/2-20, 10, "Level " + str(image.split("/")[-1][:-4]))
                    pdf.text(page_width/2-20, 30, "Across: " + str(y+1) + " of " + str(pages_down))
                    pdf.text(page_width/2-20, 20, "Down: " + str(x+1) + " of " + str(pages_across))

    pdf.output(root_path + "/data/" + session_id + "/layout.pdf", "F")
