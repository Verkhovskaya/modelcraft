import numpy as np
import os
from fpdf import FPDF
from PIL import Image
import shutil
import sys
import copy
import random
from .shared_utils import get_sections, set_render_state, get_array_section_positions
import math


def draw_level(pixel_size, block_arrays, z, section_locations, block_type_settings):
    colors = {0: [255, 255, 255], 1: [0,0,0], 2: [0,0,255], 3: [255, 0, 0], 4: [255, 0, 255], 5: [255, 255, 0], 6: [0, 255, 255], 7: [200, 200, 100]}

    other_array = block_arrays['other']
    across = other_array.shape[0]
    down = other_array.shape[1]

    color_array = np.zeros((across, down))
    color_array += other_array[:,:,z]

    if block_type_settings['water'] in ['separate']:
        color_array += 2*block_arrays['water'][:,:,z]
    if block_type_settings['lava'] in ['separate']:
        color_array += 3*block_arrays['lava'][:,:,z]
    if block_type_settings['glass'] in ['separate']:
        color_array += 4*block_arrays['glass'][:,:,z]
    if block_type_settings['fence'] in ['separate']:
        color_array += 5*block_arrays['fence'][:,:,z]
    if block_type_settings['torch'] in ['separate']:
        color_array += 6*block_arrays['torch'][:,:,z]
    if block_type_settings['ladder'] in ['separate']:
        color_array += 7*block_arrays['ladder'][:,:,z]

    image = np.zeros((down * pixel_size, across * pixel_size, 3), dtype=np.uint8) + 100
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


def generate_layout_files(root_path, session_id, block_arrays, side_length, block_type_settings, type=["pdf"]):
    for key in block_arrays.keys():
        block_arrays[key] = np.transpose(block_arrays[key], (1, 0, 2))

    section_locations = get_array_section_positions(block_arrays['other'], 10)
    image_path = root_path + "/data/" + session_id + "/layout_images"
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
    os.mkdir(image_path)

    level_image_paths = generate_level_images(root_path, session_id, image_path, block_arrays, section_locations, block_type_settings)
    generate_level_pdf(root_path, session_id, level_image_paths, side_length, block_arrays['other'].shape,
                       section_locations)


def generate_level_images(root_path, session_id, image_path, block_arrays, section_locations, block_type_settings):
    image_names = []
    z_size = block_arrays['other'].shape[2]
    for z in range(z_size):
        set_render_state(root_path, session_id, "Drawing layout image " + str(z+1) + " of " + str(z_size),int(20*z/z_size))
        data = draw_level(20, block_arrays, z, section_locations, block_type_settings)
        img = Image.fromarray(data, 'RGB')
        img_name = image_path + "/" + str(z) + ".png"
        image_names.append(img_name)
        img.save(img_name)

    return image_names


def generate_level_pdf(root_path, session_id, image_paths, side_length, array_shape, section_locations):
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
            if num_across > 1:
                spacing_x = (page_width-page_margin*2 - num_across * img_x) / (num_across-1)
            else:
                spacing_x = 0
            if num_down > 1:
                spacing_y = (page_height-page_margin*2 - num_down*(text_y+img_y)) / (num_down-1)
            else:
                spacing_y = 0

            for y in range(num_down):
                for x in range(num_across):
                    if image_paths:
                        image = image_paths.pop(0)
                        level = str(int(image.split("/")[-1][:-4])+1)
                        pdf.text(page_margin+x*spacing_x + x*img_x, page_margin+y*spacing_y-text_y+7 + y*(img_y+text_y), "Level " + level)
                        pdf.image(image, page_margin+x*spacing_x + x*img_x, page_margin+y*spacing_y + y*(img_y+text_y), array_x, array_y)

    else:
        for i in range(len(image_paths)):
            image_path = image_paths[i]
            section_size_x_units = section_locations[0][1]*20
            section_size_y_units = section_locations[1][1]*20
            section_size_x_pdf = section_size_x_units*mm/20*side_length
            section_size_y_pdf = section_size_y_units*mm/20*side_length
            num_sections_across = len(section_locations[0])-1
            num_sections_down = len(section_locations[1])-1
            sections_across = int((page_width-2.0*page_margin)/section_size_x_pdf)
            sections_down = int((page_height-2.0*page_margin)/section_size_y_pdf)
            pages_across = int(math.ceil((len(section_locations[0])-1.0)/sections_across))
            pages_down = int(math.ceil((len(section_locations[1])-1.0)/sections_down))
            for page_across in range(pages_across):
                for page_down in range(pages_down):
                    pdf.add_page()
                    original = Image.open(image_path)

                    section_start_x = page_across*sections_across + 1
                    section_start_y = page_down*sections_down + 1
                    section_end_x = min(num_sections_across, (page_across+1)*sections_across)
                    section_end_y = min(num_sections_down, (page_down+1)*sections_down)

                    left = (section_start_x-1)*section_size_x_units
                    top = (section_start_y-1)*section_size_y_units
                    right = section_end_x*section_size_x_units
                    bottom = section_end_y*section_size_y_units
                    cropped_image = original.crop((left, top, right, bottom))
                    cropped_path = image_path[:-4] + "_" + str(page_across) + "_" + str(page_down) + ".png"
                    cropped_image.save(cropped_path)

                    pdf_size_x = cropped_image.size[0]/20*mm*side_length
                    pdf_size_y = cropped_image.size[1]/20*mm*side_length

                    pdf_start_x = (page_width-pdf_size_x)/2
                    pdf_start_y = (page_height-pdf_size_y)/2

                    pdf.image(cropped_path, pdf_start_x, pdf_start_y, pdf_size_x, pdf_size_y)
                    pdf.text(page_width/2-40, 20, "Level " + str(i+1) + " / " + str(len(image_paths)))
                    pdf.text(page_width/2-40, 30, "Across: sections " +
                             str(section_start_x) + " - " + str(section_end_x) + " / " + str(num_sections_across))
                    pdf.text(page_width/2-40, 40, "Down: sections " +
                             str(section_start_y) + " - " + str(section_end_y) + " / " + str(num_sections_down))

    pdf.output(root_path + "/data/" + session_id + "/layout.pdf", "F")
