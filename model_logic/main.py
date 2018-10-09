from .generate_cutout_files import generate_laser_cut_files
from .generate_layout_files import generate_layout_files
from .get_array_from_map import get_arrays_from_map
from .file_utils import save_files
from .shared_utils import get_array_section_positions, set_render_state, request_stop_thread, label_start_thread
from time import sleep


def render(previous_thread, root_path, session_id, level_dat_file, region_files, position_file, settings_file):
    try:
        if previous_thread:
            set_render_state(root_path, session_id, "Stopping previous thread",0)
            request_stop_thread(root_path, session_id)
            while previous_thread.is_alive():
                print("Previous still running")
                sleep(0.5)
        print("start new thread")
        label_start_thread(root_path, session_id)
        set_render_state(root_path, session_id, "Saving loaded files",0)
        x1, y1, z1, x2, y2, z2 = str(position_file.file.read()).split(" ")
        save_files(root_path, session_id, level_dat_file, region_files, position_file, settings_file)
        settings_text = str(settings_file.file.read()).split("\n")
        hollow, supports = settings_text[0].split(" ")
        edit_settings = {'hollow': hollow, 'supports': supports}
        water, lava, glass, fence, torch, ladder = settings_text[2].split(" ")
        block_type_settings = {'water': water, 'lava': lava, 'glass': glass, 'fence': fence, 'torch': torch, 'ladder': ladder}
        block_arrays = get_arrays_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, edit_settings, block_type_settings)
        width, length, thickness, tab_size, piece_size = settings_text[1].split(" ")
        width, length, thickness, tab_size, piece_size = float(width), float(length), float(thickness), float(tab_size), int(piece_size)
        generate_layout_files(root_path, session_id, block_arrays, thickness, block_type_settings, type=["pdf"])
        generate_laser_cut_files(root_path, session_id, block_arrays, piece_size, 1, width, length, thickness, tab_size, block_type_settings, type=["dxf"])
        set_render_state(root_path, session_id, "done",100)

    except Exception as e:
        set_render_state(root_path, session_id, "ERROR: " + str(e), 0)