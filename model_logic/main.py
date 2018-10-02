from .generate_cutout_files import generate_laser_cut_files
from .generate_layout_files import generate_layout_files
from .get_array_from_map import get_array_from_map
from .file_utils import save_files
from .shared_utils import get_array_section_positions, set_render_state, request_stop_thread, label_start_thread
from time import sleep


def render(previous_thread, root_path, session_id, level_dat_file, region_files, position_file, settings_file):
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
    block_array = get_array_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, hollow=True)
    solid_only = lambda x: x != 0
    block_array = 1*(solid_only(block_array))
    width, length, thickness, tab_size, section_size = (settings_file.file.read()).split(" ")
    width, length, thickness, tab_size, section_size = float(width), float(length), float(thickness), float(tab_size), int(section_size)
    section_locations = get_array_section_positions(block_array, section_size)
    generate_layout_files(root_path, session_id, block_array, section_locations, thickness, type=["pdf"])
    generate_laser_cut_files(root_path, session_id, block_array, section_locations, 1, width, length, thickness, tab_size, type=["dxf"])
    set_render_state(root_path, session_id, "done",100)