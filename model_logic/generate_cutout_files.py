import sys
import numpy as np
import os
from fpdf import FPDF
from PIL import Image
import shutil
import sys
import copy
import random
import shutil
from .shared_utils import get_sections

sys.setrecursionlimit(100000)


from dxfwrite import DXFEngine as dxf

colors = {0: (255, 255, 255), 1: (139,105,20), 2: (0, 0, 255), 3: (100, 100, 100)}


def generate_laser_cut_files(root_path, session_id, block_array_one_color, section_locations, color_id, material_width, material_length, side_length, tab_size, type=["dxf"]):
    units_x = int(material_length/side_length) - 2
    units_y = int(material_width/side_length) - 2

    image_directory = root_path + "/data/" + session_id + "/cutout_images"
    if os.path.exists(image_directory):
        shutil.rmtree(image_directory)
    os.mkdir(image_directory)

    map_sections = get_sections(block_array_one_color, section_locations)
    print(map_sections)
    cutouts = get_cutouts(map_sections)
    print(cutouts)
    cutouts_placed_by_sheets = place_basic(cutouts, units_x, units_y)
    number_of_sheets_generated = len(cutouts_placed_by_sheets)
    print("Using " + str(number_of_sheets_generated) + " sheets")
    all_lines = []
    for sheet_id in range(1, number_of_sheets_generated+1):
        print(cutouts_placed_by_sheets)
        cutouts_in_sheet = list(cutouts_placed_by_sheets[sheet_id-1])
        lines = get_outlines(cutouts_in_sheet)
        lines_with_tabs = add_tabs(lines, tab_size/side_length)
        generate_png(root_path, session_id, color_id, sheet_id, units_x, units_y, 10, lines_with_tabs)
        for line in lines_with_tabs:
            all_lines.append(((line[0][0]*side_length, line[0][1]*side_length+(sheet_id-1)*material_width*1.2),
                              (line[1][0]*side_length, line[1][1]*side_length+(sheet_id-1)*material_width*1.2)))
    generate_dxf(root_path, session_id, all_lines)


def get_cutouts(map_sections):
    cutouts = []
    for section_row in map_sections:
        for section in section_row:
            for z in range(section.shape[2]):
                flat = [[Tile(section[x, y, z]) for x in range(section.shape[0])] for y in range(section.shape[1])]
                for x in range(section.shape[0]):
                    for y in range(section.shape[1]):
                        cutout = spread(flat, x, y)
                        if cutout != []:
                            min_x = min([a[0] for a in cutout])
                            max_x = max([a[0] for a in cutout])
                            min_y = min([a[1] for a in cutout])
                            max_y = max([a[1] for a in cutout])
                            cutout_array = np.zeros((int(max_x - min_x + 1), int(max_y - min_y + 1)), dtype=bool)
                            for x in range(cutout_array.shape[0]):
                                for y in range(cutout_array.shape[1]):
                                    cutout_array[x, y] = (x + min_x, y + min_y) in cutout
                            cutouts.append(cutout_array)
    return cutouts


def add_tabs(lines, tab_unit_size):
    original_lines = set(lines)
    new_lines = []
    for line in lines:
        print("Line: " + str(line))
        line_vector = ((line[1][0]-line[0][0]), (line[1][1]-line[0][1]))
        print("Line vector: " + str(line_vector))
        print("Tab size: " + str(tab_unit_size))
        if line_vector[1] == 0:
            if ((line[0][0], line[0][1]), (line[0][0], line[0][1]+1)) in original_lines or \
                ((line[0][0], line[0][1]+1), (line[0][0], line[0][1])) in original_lines:
                new_lines.append(((line[0][0], line[0][1]),\
                    (line[0][0]+line_vector[0]*(1-tab_unit_size)/2, line[0][1]+line_vector[1]*(1-tab_unit_size)/2)))
                new_lines.append(((line[1][0], line[1][1]), \
                                 (line[1][0] - line_vector[0] * (1 - tab_unit_size) / 2,
                                  line[1][1] - line_vector[1] * (1 - tab_unit_size) / 2)))
            else:
                if random.random()*4 < 1:
                    new_lines.append(((line[0][0], line[0][1]),\
                        (line[0][0]+line_vector[0]*(1-tab_unit_size)/2, line[0][1]+line_vector[1]*(1-tab_unit_size)/2)))
                    new_lines.append(((line[1][0], line[1][1]), \
                                     (line[1][0] - line_vector[0] * (1 - tab_unit_size) / 2,
                                      line[1][1] - line_vector[1] * (1 - tab_unit_size) / 2)))
                else:
                    new_lines.append(line)
        else:
            if random.random()*4 < 1:
                new_lines.append(((line[0][0], line[0][1]),\
                    (line[0][0]+line_vector[0]*(1-tab_unit_size)/2, line[0][1]+line_vector[1]*(1-tab_unit_size)/2)))
                new_lines.append(((line[1][0], line[1][1]), \
                                 (line[1][0] - line_vector[0] * (1 - tab_unit_size) / 2,
                                  line[1][1] - line_vector[1] * (1 - tab_unit_size) / 2)))
            else:
                new_lines.append(line)

    return new_lines


class Tile:
    def __init__(self, type):
        self.seen = False
        self.type = type


def spread(flat, x, y):
    if x < 0 or x >= len(flat[0]) or y < 0 or y >= len(flat):
        return []
    if flat[y][x].seen or not flat[y][x].type:
        return []
    flat[y][x].seen = True
    visited = []
    visited += spread(flat, x + 1, y)
    visited += spread(flat, x, y + 1)
    visited += spread(flat, x - 1, y)
    visited += spread(flat, x, y - 1)
    visited.append((x, y))
    return visited



class Cutout():
    def __init__(self, array, x, y):
        self.array = array
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class Sheet:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.array = np.zeros((x_size, y_size), dtype=bool)
        # TODO: Fix this down here. It technically should be just x_size, but whatever
        self.empty_verticals = [x_size-1 for y in range(y_size)]
        self.cutouts = []

    def place(self, cutout):
        for y in range(self.array.shape[1] - cutout.shape[1]):
            if self.empty_verticals[y] >= cutout.shape[0]:
                for x in range(self.array.shape[0] - cutout.shape[0]):
                    for rotate in range(1):
                        rotated_cutout = np.rot90(cutout, k=rotate, axes=(0, 1))
                        if y + rotated_cutout.shape[1] < self.y_size and x + rotated_cutout.shape[0] < self.x_size:
                            if not True in self.array[x:x + rotated_cutout.shape[0], y:y + rotated_cutout.shape[1]] * rotated_cutout:
                                self.array[x:x + rotated_cutout.shape[0], y:y + rotated_cutout.shape[1]] += rotated_cutout
                                for y_level in range(rotated_cutout.shape[1]):
                                    self.empty_verticals[y+y_level] -= sum(rotated_cutout[:,y_level])
                                print(self.empty_verticals[:10])
                                self.cutouts.append(Cutout(cutout, x, y))
                                return

        raise Exception("Could not place. cutout: " + str(cutout) + ", empty verticals: " + str(self.empty_verticals))


def place_basic(cutouts, units_x, units_y):
    sheets = [Sheet(units_x, units_y)]
    cutouts_by_height = sorted(cutouts, key=lambda cutout: cutout.shape[1])[::-1]
    cutouts_with_placement = []
    i = 0
    for new_cutout in cutouts_by_height:
        print(i)
        i += 1
        placed = False
        for sheet in sheets:
            try:
                print("HO")
                sheet.place(new_cutout)
                placed = True
                break
            except Exception as e:
                pass
        if not placed:
            new_sheet = Sheet(units_x, units_y)
            new_sheet.place(new_cutout)
            sheets.append(new_sheet)
    return [sheet.cutouts for sheet in sheets]


def get_outlines(cutouts):
    all_lines = set()
    for cutout in cutouts:
        outline = set()
        for x in range(cutout.array.shape[0]):
            for y in range(cutout.array.shape[1]):
                if cutout.array[x,y]:
                    block = (x+cutout.x, y+cutout.y)
                    line0 = ((block[0], block[1]), (block[0], block[1] + 1))
                    line1 = ((block[0], block[1]), (block[0] + 1, block[1]))
                    line2 = ((block[0] + 1, block[1]), (block[0] + 1, block[1] + 1))
                    line3 = ((block[0], block[1] + 1), (block[0] + 1, block[1] + 1))
                    for line in [line0, line1, line2, line3]:
                        if line in outline:
                            outline.remove(line)
                        else:
                            outline.add(line)
        for line in outline:
            all_lines.add(line)
    return list(all_lines)


def generate_dxf(root_path, session_id, all_lines):
    drawing = dxf.drawing(root_path + "/data/" + session_id + '/cutout.dxf')
    drawing.add_layer('LINES')

    for line in all_lines:
        start = (line[0][0], line[0][1])
        end = (line[1][0], line[1][1])
        drawing.add(dxf.line(start, end, color=2))
    drawing.save()


def generate_png(root_path, session_id, color_id, sheet_id, units_x, units_y, render_unit_length, lines):
    image = np.zeros(((units_y+2) * render_unit_length, (units_x + 2) * render_unit_length, 3), dtype=np.uint8)
    for line in lines:
        start = min(line[0][0], line[1][0])+1, min(line[0][1], line[1][1])+1
        end = max(line[0][0], line[1][0])+1, max(line[0][1], line[1][1])+1
        image[int(render_unit_length*start[1])-2:int(render_unit_length*end[1])+2,
              int(render_unit_length*start[0])-2:int(render_unit_length*end[0])+2] = (255, 255, 255)

    img = Image.fromarray(image, 'RGB')
    img_name = root_path + "/data/" + session_id + "/cutout_images/" + str(color_id) + "_" + str(sheet_id) + "_cutout.png"
    img.save(img_name)
