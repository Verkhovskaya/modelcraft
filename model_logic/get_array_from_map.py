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
    hollow_blocks = [0]
    hollow_array = copy.copy(color_array)
    for z_minus in range(2, color_array.shape[2]+1):
        z = color_array.shape[2]-z_minus
        for x in range(1,color_array.shape[0]-1):
            for y in range(1, color_array.shape[1]-1):
                if int(color_array[x-1,y-1,z+1]) not in hollow_blocks and\
                        int(color_array[x,y-1,z+1]) not in hollow_blocks and\
                        int(color_array[x+1,y-1,z+1]) not in hollow_blocks and\
                        int(color_array[x+1,y,z+1]) not in hollow_blocks and\
                        int(color_array[x+1,y+1,z+1]) not in hollow_blocks and\
                        int(color_array[x,y+1,z+1]) not in hollow_blocks and\
                        int(color_array[x-1,y+1,z+1]) not in hollow_blocks and\
                        int(color_array[x-1,y,z+1]) not in hollow_blocks:
                    hollow_array[x, y, z] = 0

    return hollow_array


def add_supports(main_array):
    z = main_array.shape[2]
    non_zero = np.vectorize(lambda x: 1*(x != 0))
    supports_array = np.copy(main_array)
    supports_array[:,:,:z-1] += supports_array[:,:,1:z]
    supports_array = make_hollow(supports_array)
    main_array += supports_array
    return non_zero(main_array)


class AttributeHolder():
    pass


def get_arrays_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, edit_settings, block_type_settings):
    x_min = min(int(x1), int(x2))
    x_max = max(int(x1), int(x2))
    y_min = min(int(y1), int(y2))
    y_max = max(int(y1), int(y2))
    z_min = min(int(z1), int(z2))
    z_max = max(int(z1), int(z2))

    x_diff = x_max - x_min
    y_diff = y_max - y_min
    z_diff = z_max - z_min

    if True:
        level = pymclevel_copy.mclevel.fromFile(root_path + "/data/" + session_id + "/map")
        block_array = np.zeros((x_diff, y_diff, z_diff))
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                chunk = level.getChunk(x / 16, y / 16)
                block = chunk.Blocks[x % 16, y % 16, z_min:z_max].astype(int)
                block_array[x - x_min, y - y_min, :] = block

        is_water = np.vectorize(lambda x: 1*(x in [8,9,79]))
        is_lava = np.vectorize(lambda x: 1*(x in [10,11]))
        is_glass = np.vectorize(lambda x: 1*(x in [20,241]))
        is_fence = np.vectorize(lambda x: 1*(x in [85, 113]))
        is_torch = np.vectorize(lambda x: 1*(x in [50]))
        is_ladder = np.vectorize(lambda x: 1*(x in [65]))
        is_not_air = np.vectorize(lambda x: 1*(x != 0))

        water_array = is_water(block_array)
        lava_array = is_lava(block_array)
        glass_array = is_glass(block_array)
        fence_array = is_fence(block_array)
        torch_array = is_torch(block_array)
        ladder_array = is_ladder(block_array)

        other_array = is_not_air(block_array)
        if block_type_settings['water'] != 'main':
            other_array -= water_array
        if block_type_settings['lava'] != 'main':
            other_array -= lava_array
        if block_type_settings['glass'] != 'main':
            other_array -= glass_array
        if block_type_settings['fence'] != 'main':
            other_array -= fence_array
        if block_type_settings['torch'] != 'main':
            other_array -= torch_array
        if block_type_settings['ladder'] != 'main':
            other_array -= ladder_array

        if edit_settings['supports'] == "true":
            other_array = add_supports(other_array)
        if edit_settings['hollow'] == "true":
            other_array = make_hollow(other_array)

        print("Success!")
        return {'water': water_array, 'lava': lava_array, 'glass': glass_array, 'fence': fence_array,
                'torch': torch_array, 'ladder': ladder_array, 'other': other_array}

        """
    except Exception as e:
        print(e)
        world = AttributeHolder()
        world.materials = pymclevel2_copy.materials.BlockstateMaterials()
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
                    world.materials = pymclevel2_copy.anvil2.BlockstateMaterials()
                    regions[(region_x, region_y)] = pymclevel2_copy.anvil2.BlockstateRegionFile(world,
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
            """