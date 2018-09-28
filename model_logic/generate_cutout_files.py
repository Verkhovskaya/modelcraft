import sys
import numpy as np
import os
from fpdf import FPDF
from PIL import Image
import shutil
import sys
import copy
import random

sys.setrecursionlimit(100000)


from dxfwrite import DXFEngine as dxf

colors = {0: (255, 255, 255), 1: (139,105,20), 2: (0, 0, 255), 3: (100, 100, 100)}
segment_size = 3
map_x = 100

def generate_cutout_files(root_path, session_id, color_array, type=["dxf"]):
    colors = np.unique(color_array)
    print("Colors: " + str(colors))
    cutouts_by_color = []
    for color in colors:
        if color != 0:
            print("For colour " + str(color))
            print("Generating mask array")
            mask_array = (color_array == color)
            print("Getting cutouts")
            color_cutouts = []
            all_cutouts = []
            for x in range(mask_array.shape[0]/segment_size+1):
                for y in range(mask_array.shape[1]/segment_size+1):
                    cutouts = get_cutouts(mask_array[segment_size*x:segment_size+segment_size*x, segment_size*y:segment_size+segment_size*y, :])
                    all_cutouts += cutouts
            cutouts_class = place_basic(all_cutouts, x, mask_array.shape[0]/segment_size+1, y, mask_array.shape[1]/segment_size+1, map_x)
            temp_outlines = get_outlines(cutouts_class)
            print temp_outlines
            for cutout in cutouts_class:
                for x_slide in range(cutout.array.shape[0]):
                    if cutout.array[x_slide, 0]:
                        x_at = x_slide
                        break
                temp_outlines.remove(((cutout.x+x_at, cutout.y), (cutout.x+x_at, cutout.y+1)))
                temp_outlines.add(((cutout.x+x_at, cutout.y), (cutout.x+x_at, cutout.y+0.4)))
                temp_outlines.add(((cutout.x+x_at, cutout.y+0.6), (cutout.x+x_at, cutout.y+1)))
            for cutout in cutouts_class:
                for y_slide in range(cutout.array.shape[1]):
                    if cutout.array[0, y_slide]:
                        y_at = y_slide
                        break
                temp_outlines.remove(((cutout.x, cutout.y+y_at), (cutout.x+1, cutout.y + y_at)))
                temp_outlines.add(((cutout.x, cutout.y+y_at), (cutout.x+0.4, cutout.y + y_at)))
                temp_outlines.add(((cutout.x+0.6, cutout.y+y_at), (cutout.x+1, cutout.y + y_at)))
            for cutout in cutouts_class:
                for x_slide in range(cutout.array.shape[0]):
                    if cutout.array[x_slide, cutout.array.shape[1]-1]:
                        x_at = x_slide
                        break
                if ((cutout.x+x_at+1, cutout.y+cutout.array.shape[1]-1), (cutout.x+x_at+1, cutout.y+cutout.array.shape[1])) in temp_outlines:
                    temp_outlines.remove(((cutout.x+x_at+1, cutout.y+cutout.array.shape[1]-1), (cutout.x+x_at+1, cutout.y+cutout.array.shape[1])))
                    temp_outlines.add(((cutout.x+x_at+1, cutout.y+cutout.array.shape[1]-1), (cutout.x+x_at+1, cutout.y+cutout.array.shape[1]-0.6)))
                    temp_outlines.add(((cutout.x+x_at+1, cutout.y+cutout.array.shape[1]-0.4), (cutout.x+x_at+1, cutout.y+cutout.array.shape[1])))
            change = []
            for outline in temp_outlines:
                if random.random() < 0.2:
                    change.append(outline)
            for outline in change:
                    if outline[1] == (outline[0][0], outline[0][1]+1):
                        temp_outlines.remove(outline)
                        temp_outlines.add(((outline[0][0], outline[0][1]), (outline[0][0], outline[0][1]+0.4)))
                        temp_outlines.add(((outline[0][0], outline[0][1]+0.6), (outline[0][0], outline[0][1]+1)))
                    if outline[1] == (outline[0][0]+1, outline[0][1]):
                        temp_outlines.remove(outline)
                        temp_outlines.add(((outline[0][0], outline[0][1]), (outline[0][0] + 0.4, outline[0][1])))
                        temp_outlines.add(((outline[0][0] + 0.6, outline[0][1]), (outline[0][0] + 1, outline[0][1])))
            color_cutouts.append(temp_outlines)

            print("Placing basic")
            print("Getting outlines")
            cutouts_by_color.append(color_cutouts)
    print("Generating dxf")
    generate_dxf(root_path, session_id, cutouts_by_color)
    generate_png(root_path, session_id, cutouts_by_color)



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


def get_cutouts(mask_array):
    cutouts = []
    for z in range(mask_array.shape[2]):
        flat = [[Tile(mask_array[x, y, z]) for x in range(mask_array.shape[0])] for y in range(mask_array.shape[1])]
        for x in range(mask_array.shape[0]):
            for y in range(mask_array.shape[1]):
                cutout = spread(flat, x, y)
                if cutout != []:
                    min_x = min([a[0] for a in cutout])
                    max_x = max([a[0] for a in cutout])
                    min_y = min([a[1] for a in cutout])
                    max_y = max([a[1] for a in cutout])
                    cutout_array = np.zeros((int(max_x-min_x+1), int(max_y-min_y+1)), dtype=bool)
                    for x in range(cutout_array.shape[0]):
                        for y in range(cutout_array.shape[1]):
                            cutout_array[x,y] = (x+min_x,y+min_y) in cutout
                    cutouts.append(cutout_array)
    return cutouts

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
                                return Cutout(rotated_cutout, x, y)
        print("Could not place!!")

def place_basic(cutouts, x, x_max, y, y_max, map_x):
    sheet = Sheet(map_x, map_x*5)

    cutouts_by_height = sorted(cutouts, key=lambda cutout: cutout.shape[1])[::-1]

    cutouts_with_placement = []
    count = 1
    total = len(cutouts_by_height)

    for new_cutout in cutouts_by_height:
        cutouts_with_placement.append(sheet.place(new_cutout))
        print("Placing " + str(count) + " of " + str(total) + " (x: " + str(x) + " of " + str(x_max) + ", y: " + str(y) + " of " + str(y_max) + ")")
        count += 1

    return cutouts_with_placement


def get_outlines(all_cutouts):
    outlines = set()
    for cutout in all_cutouts:
        outline = set()
        for x in range(cutout.array.shape[0]):
            for y in range(cutout.array.shape[1]):
                if cutout.array[x,y]:
                    block = (x+cutout.x, y+cutout.y)
                    line0 = ((block[0], block[1]), (block[0], block[1] + 1))
                    line1 = ((block[0], block[1]), (block[0] + 1, block[1]))
                    line2 = ((block[0] + 1, block[1]), (block[0] + 1, block[1] + 1))
                    line3 = ((block[0], block[1] + 1), (block[0] + 1, block[1] + 1))
                    if line0 in outline:
                        outline.remove(line0)
                    else:
                        outline.add(line0)
                    if line1 in outline:
                        outline.remove(line1)
                    else:
                        outline.add(line1)
                    if line2 in outline:
                        outline.remove(line2)
                    else:
                        outline.add(line2)
                    if line3 in outline:
                        outline.remove(line3)
                    else:
                        outline.add(line3)
        for line in outline:
            if line not in outlines:
                outlines.add(line)
    return outlines

def generate_dxf(root_path, session_id, outlines_by_color):
    drawing = dxf.drawing(root_path + "/data/" + session_id + '/cutout.dxf')
    drawing.add_layer('LINES')

    for color in range(len(outlines_by_color)):
        for segment_id in range(len(outlines_by_color[color])):
            for line in outlines_by_color[color][segment_id]:
                start = (line[0][0]+color*(map_x+10), line[0][1]+300*segment_id)
                end = (line[1][0]+color*(map_x+10), line[1][1]+300*segment_id)
                drawing.add(dxf.line(start, end, color=7))
    drawing.save()

def generate_png(root_path, session_id, outlines_by_color):
    length_x = max(max(max(max(point[0] for point in line) for line in segment) for segment in color) for color in outlines_by_color)
    length_y = max(max(max(max(point[1] for point in line) for line in segment) for segment in color) for color in outlines_by_color)
    print(length_x, length_y)
    side_length = 10
    image = np.zeros(((length_y+2) * side_length, (length_x + 2) * side_length, 3), dtype=np.uint8)
    for color in range(len(outlines_by_color)):
        for segment_id in range(len(outlines_by_color[color])):
            for line in outlines_by_color[color][segment_id]:
                start = min(line[0][0], line[1][0])+1, min(line[0][1], line[1][1])+1
                end = max(line[0][0], line[1][0])+1, max(line[0][1], line[1][1])+1
                image[int(side_length*start[1])-2:int(side_length*end[1])+2,
                      int(side_length*start[0])-2:int(side_length*end[0])+2] = (255, 255, 255)

    img = Image.fromarray(image, 'RGB')
    img_name = root_path + "/data/" + session_id + "/cutout.png"
    img.save(img_name)
