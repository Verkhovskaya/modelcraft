from bottle import route, request, static_file, run, post
import uuid
import sys
import time
import os

sys.setrecursionlimit(100000)
root_path = str(os.getcwd())
#source: google
#info in: None
#info out: session id
#backend: generate user folder (upload_map)
#next: upload_map, order_status
@route('/')
def root():
	session_id = str(uuid.uuid4())


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
	print(request.files.__dict__)
	time.sleep(3)

#----------------------- Serve files


@route('/favicon')
def favicon():
	return static_file("favicon.jpeg", root=root_path)

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

@route('/serve_icon/<session_id>')
def serve_icon(session_id):
	return static_file("icon.png", root=root_path + "/data/" + session_id + "/map")

@route('/root_image')
def root_image():
	return static_file("house.jpeg", root=root_path)


try:
	run(host='0.0.0.0', port=80, debug=True)
except:
	run(host='localhost', port=8080, debug=True)
