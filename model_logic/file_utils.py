import os
import shutil
import time
import datetime

def create_session(root_path, session_id, request):
    data_directory = root_path + "/data"
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)

    session_directory = data_directory + "/" + session_id
    if not os.path.exists(session_directory):
        os.mkdir(session_directory)

    image_directory = session_directory + "/cutout_images"
    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    request_info = open(session_directory + "/session_info.txt", "w")
    timestamp = datetime.datetime.fromtimestamp(time.time())\
        .strftime('%Y-%m-%d %H:%M:%S')
    request_info.write(timestamp + "\n")
    request_info.write(request.environ.get('REMOTE_ADDR'))
    request_info.close()

def save_files(root_path, session_id, level_dat_file, region_files, position_file, settings_file):
    if not position_file:
        raise Exception("Missing position file")
    if not level_dat_file:
        raise Exception("Missing level.dat file")
    if not region_files:
        raise Exception("Missing region files")
    if not settings_file:
        raise Exception("Missing settings file")

    session_directory = root_path + "/data/" + session_id

    if os.path.isfile(session_directory + "/position.txt"):
            os.remove(session_directory + "/position.txt")
    position_file.save(session_directory)

    if os.path.isfile(session_directory + "/settings.txt"):
            os.remove(session_directory + "/settings.txt")
    settings_file.save(session_directory)

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