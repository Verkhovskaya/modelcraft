from bottle import route, request, static_file, run, post
import uuid
import sys
import time
import os
import model_logic
import threading
from model_logic import file_utils

root_path = str(os.getcwd())
if root_path == "/root":
    root_path = "/Users/2017-A/Dropbox/web_dev/modelcraft"

@route('/')
def root():
    session_id = str(uuid.uuid4())
    file_utils.create_session(root_path, session_id)
    text = open(root_path + "/html/header.html", "r").read() + \
           open(root_path + "/html/session_id.html", "r").read().replace("$$session_id$$", session_id) + \
           open(root_path + "/html/0_description.html", "r").read() + \
           open(root_path + "/html/1_upload_map.html", "r").read() + \
           open(root_path + "/html/2_pick_location.html", "r").read() + \
           open(root_path + "/html/advanced_settings.html", "r").read() + \
           open(root_path + "/html/3_laser_cut.html", "r").read()\
               .replace("$$session_id$$", session_id)\
               .replace("$$session_id$$", session_id) + \
           open(root_path + "/html/4_build.html", "r").read()\
               .replace("$$session_id$$", session_id) \
               .replace("$$session_id$$", session_id)+ \
           open(root_path + "/html/footer.html", "r").read()
    return text


render_threads = {}
@post('/request_render')
def request_render():
    print("requesting render")
    level_dat_file = request.files["level_dat"]
    session_id_file = request.files["session_id"]
    session_id = str(session_id_file.file.read())
    position_file = request.files["position"]
    settings_file = request.files["settings"]
    region_file_names = filter(lambda x: x not in ["level_dat", "session_id", "position", "settings"], request.files.keys())
    region_files = [request.files[x] for x in region_file_names]
    new_thread = threading.Thread(target = model_logic.render, args=(
        render_threads.get(session_id, None), root_path, session_id, level_dat_file, region_files, position_file, settings_file))
    new_thread.start()
    render_threads[session_id] = new_thread
    print("Started thread")


@route('/available_cutouts/<session_id>/<cache_breaker>')
def stylesheet(session_id, cache_breaker):
    cutout_file_names = os.listdir(root_path + "/data/" + session_id + "/cutout_images")
    cutouts = {}
    for name in cutout_file_names:
        color_id, sheet_id, _ = name.split("_")
        if color_id not in cutouts.keys():
            cutouts[color_id] = []
        cutouts[color_id].append(sheet_id)
    return {"data": cutouts}


#----------------------- Serve files


@route('/favicon')
def favicon():
    return static_file("favicon.jpeg", root=root_path + "/graphics")

@route('/layout_front_page')
def stylesheet():
    return static_file("script.js", root=root_path + "/javascript")

@route('/layout_image/<session_id>/<level>/<cache_breaker>')
def stylesheet(session_id, level, cache_breaker):
    return static_file(str(level) + ".png", root=root_path + "/data/" + session_id + "/layout_images")

@route('/download_layout_pdf/<session_id>')
def serve_layout_pdf(session_id):
    return static_file("layout.pdf", root=root_path + "/data/" + session_id, download="layout.pdf")

@route('/cutout_image/<session_id>/<color_id>/<sheet_id>/<cache_breaker>')
def stylesheet(session_id, color_id, sheet_id, cache_breaker):
    return static_file(color_id + "_" + sheet_id + "_cutout.png", root=root_path + "/data/" + session_id + "/cutout_images")

@route("/download_laser_cut_dxf/<session_id>")
def dxf(session_id):
    return static_file("cutout.dxf", root=root_path + "/data/"+session_id, download="cutout.dxf")

@route('/render_state/<session_id>/<cache_breaker>')
def renderstate(session_id, cache_breaker):
    return open(root_path + "/data/" + session_id + "/render_state.txt").read()

@route('/get_stylesheet')
def stylesheet():
    return static_file("stylesheet.css", root=root_path + "/css")

@route('/javascript_functions')
def stylesheet():
    return static_file("script.js", root=root_path + "/javascript")

@route('/root_image')
def root_image():
    return static_file("house.jpeg", root=root_path + "/graphics")

@route('/corners_graphic')
def corners_graphic():
    return static_file("BoxGraphic.png", root=root_path + "/graphics")

@route('/stop')
def stop():
    raise Exception("Stopping all")

@route('/sitemap')
def corners_graphic():
    return static_file("sitemap.xml", root=root_path)

try:
    run(host='0.0.0.0', port=80, debug=True, server="paste")
except:
    run(host='localhost', port=8080, debug=True)
