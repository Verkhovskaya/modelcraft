
def set_render_state(root_path, session_id, new_state, load_progression):
    if open(root_path + "/data/" + session_id + "/render_state.txt", "r").read() == "Stop previous thread\n0":
        raise Exception("Stopping thread")
    render_state_file = open(root_path + "/data/" + session_id + "/render_state.txt", "w")
    render_state_file.write(new_state+"\n"+str(load_progression))
    render_state_file.close()


def get_array_section_positions(block_array, max_size):
    extra_x = block_array.shape[0]%max_size
    extra_y = block_array.shape[1]%max_size
    array_x = block_array.shape[0]
    array_y = block_array.shape[1]
    x_cuts = [i*max_size for i in range(array_x/max_size+1)]
    y_cuts = [i*max_size for i in range(array_y/max_size+1)]

    if (float(extra_x)/max_size < 0.5) & (len(x_cuts) > 1):
        x_cuts[-1] = array_x
    else:
        x_cuts.append(array_x)
    if (float(extra_y) / max_size < 0.5) & (len(y_cuts) > 1):
        y_cuts[-1] = array_y
    else:
        y_cuts.append(array_y)
    return x_cuts, y_cuts


def get_sections(block_array, section_locations):
    map_sections = []
    x_cuts = section_locations[0]
    y_cuts = section_locations[1]
    for y in range(len(y_cuts)-1):
        map_sections.append([])
        for x in range(len(x_cuts)-1):
            map_sections[-1].append(block_array[x_cuts[x]:x_cuts[x+1], y_cuts[y]:y_cuts[y+1]])

    print(x_cuts, y_cuts)
    return map_sections


def label_start_thread(root_path, session_id):
    thread_file = open(root_path + "/data/" + session_id + "/render_state.txt", "w")
    thread_file.write("Request render\n0")
    thread_file.close()


def request_stop_thread(root_path, session_id):
    thread_file = open(root_path + "/data/" + session_id + "/render_state.txt", "w")
    thread_file.write("Stop previous thread\n0")
    thread_file.close()