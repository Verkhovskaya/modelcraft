from bottle import route, request, static_file, run, post
import uuid
import sys
import time
import os
import model_logic

root_path = str(os.getcwd())

@route('/')
def root():
    session_id = str(uuid.uuid4())
    print(session_id)
    text = open(root_path + "/html/header.html", "r").read() + \
           open(root_path + "/html/session_id.html", "r").read().replace("$$session_id$$", session_id) + \
           open(root_path + "/html/0_description.html", "r").read() + \
           open(root_path + "/html/1_upload_map.html", "r").read() + \
           open(root_path + "/html/2_pick_location.html", "r").read() + \
           open(root_path + "/html/3_results.html", "r").read() + \
           open(root_path + "/html/footer.html", "r").read()
    return text

@post('/request_render')
def request_render():
    print("requesting render")
    level_dat_file = request.files["level_dat"]
    session_id_file = request.files["session_id"]
    position_file = request.files["position"]
    region_file_names = filter(lambda x: x not in ["level_dat", "session_id", "position"], request.files.keys())
    region_files = [request.files[x] for x in region_file_names]

    model_logic.render(root_path, session_id_file, level_dat_file, region_files, position_file)


#----------------------- Serve files


@route('/favicon')
def favicon():
    return static_file("favicon.jpeg", root=root_path + "/graphics")

@route('/show_layout_pdf/<session_id>')
def serve_layout_pdf(session_id):
    return static_file("layout.pdf", root=root_path)

@route('/show_cutout_pdf/<session_id>')
def serve_layout_pdf(session_id):
    return static_file("layout.pdf", root=root_path)

@route('/download_layout_pdf/<session_id>')
def serve_layout_pdf(session_id):
    return static_file("layout.pdf", root=root_path + "/data/" + session_id, download="layout.pdf")

@route("/download_dxf/<session_id>")
def dxf(session_id):
    return static_file("cutout.dxf", root=root_path + "/data/"+session_id, download="cutout.dxf")

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

try:
    run(host='0.0.0.0', port=80, debug=True)
except:
    run(host='localhost', port=8080, debug=True)
