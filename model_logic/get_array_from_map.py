try:
    from external_libraries import pymclevel_copy
except Exception as e:
    print("Could not import parcer for v.12")

try:
    from external_libraries import pymclevel2_copy
except Exception as e:
    print("Could not import parcer for v.13")
import numpy as np
import copy


def make_hollow(color_array):
    hollow_array = copy.copy(color_array)
    for z_minus in range(2, color_array.shape[2]+1):
        z = color_array.shape[2]-z_minus
        for x in range(1,color_array.shape[0]-1):
            for y in range(1, color_array.shape[1]-1):
                if int(color_array[x-1,y,z+1]) == 1 and int(color_array[x+1,y,z+1]) == 1:
                    if int(color_array[x,y-1,z+1]) == 1 and int(color_array[x,y+1,z+1]) == 1:
                        if int(color_array[x+1,y-1,z+1]) == 1 and int(color_array[x+1,y+1,z+1]) == 1:
                            if int(color_array[x-1,y-1,z+1]) == 1 and int(color_array[x-1,y+1,z+1]) == 1:
                                if color_array[x,y,z+1] == 1:
                                    hollow_array[x,y,z] = 0
    return hollow_array


class AttributeHolder():
    pass


def get_array_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, settings_text):
    hollow, supports = settings_text[0].split(" ")
    hollow = (hollow == "true")
    supports = (supports == "true")

    x_min = min(int(x1), int(x2))
    x_max = max(int(x1), int(x2))
    y_min = min(int(y1), int(y2))
    y_max = max(int(y1), int(y2))
    z_min = min(int(z1), int(z2))
    z_max = max(int(z1), int(z2))

    x_diff = x_max - x_min
    y_diff = y_max - y_min
    z_diff = z_max - z_min

    try:
        level = pymclevel.mclevel.fromFile(root_path + "/data/" + session_id + "/map")
        block_array = np.zeros((x_diff, y_diff, z_diff))
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                chunk = level.getChunk(x / 16, y / 16)
                block = chunk.Blocks[x % 16, y % 16, z_min:z_max].astype(int)
                block_array[x - x_min, y - y_min, :] = block

    except Exception as e:
        world = AttributeHolder()
        world.materials = pymclevel2_13.materials.BlockstateMaterials()
        # setattr(world, 'materials', anvil2.BlockstateMaterials())
        # 10_10_chunks_per_region
        #  16_16_chunk

        regions = {}
        chunks = {}

        block_array = np.zeros((x_diff, y_diff, z_diff))

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                region_x = x/160
                region_y = y/160
                if (region_x, region_y) not in regions.keys():
                    world = AttributeHolder()
                    world.materials = pymclevel2_13.anvil2.BlockstateMaterials()
                    regions[(region_x, region_y)] = pymclevel2_13.anvil2.BlockstateRegionFile(world,
                        root_path + "/data/" + session_id + "/map/region/r." + str(region_x) + "." + str(region_y) + ".mca")

                chunk_x = x % 10
                chunk_y = y % 10
                if (region_x, region_y, chunk_x, chunk_y) not in chunks.keys():
                    to_string = np.vectorize(lambda x: str(x))
                    try:
                        chunk = regions[(region_x, region_y)].getChunk(chunk_x, chunk_y)
                        block_names = to_string(chunk.Blocks[chunk_x, z_min: z_max, chunk_y])
                        print block_names
                        blocks = block_names != 'air'
                        block_array[x-x_min, y-y_min, :] = blocks
                    except AttributeError as e:
                        print("Could not find region " + str((region_x, region_y)) +", chunk " + str((chunk_x, chunk_y)))

    if hollow:
        block_array = make_hollow(block_array)
    return block_array
