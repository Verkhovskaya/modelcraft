import os
import shutil


def save_files(root_path, session_id, level_dat_file, region_files, position_file):
    if not position_file:
        raise Exception("Missing postiion file")
    if not level_dat_file:
        raise Exception("Missing level.dat file")
    if not region_files:
        raise Exception("Missing region files")

    data_directory = root_path + "/data"
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)

    session_directory = data_directory + "/" + session_id
    if not os.path.exists(session_directory):
        os.mkdir(session_directory)

    if os.path.isfile(session_directory + "/position.txt"):
            os.remove(session_directory + "/position.txt")
    position_file.save(session_directory)

    map_directory = session_directory + "/map"
    if os.path.exists(map_directory):
        shutil.rmtree(map_directory)
    os.mkdir(map_directory)

    level_dat_file.save(map_directory)

    region_directory = map_directory + "/region"
    os.mkdir(region_directory)
    for region_file in region_files:
        if os.path.isfile(region_directory + "/" + region_file.filename):
            os.remove(region_directory + "/" + region_file.filename)
        region_file.save(region_directory)


def delete_map_files(root_path, session_id):
    shutil.rmtree(root_path + "/" + session_id + "/map")


def delete_all_files(root_path, session_id):
    shutil.rmtree(root_path + "/" + session_id)