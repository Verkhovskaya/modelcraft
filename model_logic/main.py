from .generate_cutout_files import generate_cutout_files
from .generate_layout_files import generate_layout_files
from .get_array_from_map import get_array_from_map
from .file_utils import save_files


def render(root_path, session_id_file, level_dat_file, region_files, position_file):
    session_id = str(session_id_file.file.read())
    save_files(root_path, session_id, level_dat_file, region_files, position_file)
    x1, y1, z1, x2, y2, z2 = str(position_file.file.read()).split(" ")
    block_array = get_array_from_map(root_path, session_id, x1, y1, z1, x2, y2, z2, hollow=True)
    generate_layout_files(root_path, session_id, block_array, type=["pdf"])
    generate_cutout_files(root_path, session_id, block_array, type=["dxf"])