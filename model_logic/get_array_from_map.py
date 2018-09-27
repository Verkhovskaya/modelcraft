
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


def get_array_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, hollow=True):
    x_min = min(int(x1), int(x2)) - 1
    x_max = max(int(x1), int(x2)) + 1
    y_min = min(int(y1), int(y2)) - 1
    y_max = max(int(y1), int(y2)) + 1
    z_min = min(int(z1), int(z2))
    z_max = max(int(z1), int(z2))

    x_diff = x_max - x_min
    y_diff = y_max - y_min
    z_diff = z_max - z_min

    level = mclevel.fromFile(root_path + "/data/" + session_id + "/map")

    block_array = np.zeros((x_diff, y_diff, z_diff))

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            chunk = level.getChunk(x / 16, y / 16)
            block = chunk.Blocks[x % 16, y % 16, z_min:z_max].astype(int)
            block_array[x - x_min, y - y_min, :] = block

    if hollow:
        block_array = make_hollow(block_array)

    return block_array

