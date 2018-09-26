from bottle import route, request, static_file, run, post
import uuid
import sys
import time


sys.setrecursionlimit(100000)
#source: google
#info in: None
#info out: session id
#backend: generate user folder (upload_map)
#next: upload_map, order_status
@route('/')
def root():
	session_id = str(uuid.uuid4())

	root = "/Users/2017-A/Dropbox/web_dev/modelcraft"

	text = open(root + "/html/header.html", "r").read() + \
		   open(root + "/html/session_id.html", "r").read().replace("$$session_id$$", session_id) + \
		   open(root + "/html/0_description.html", "r").read() + \
		   open(root + "/html/1_upload_map.html", "r").read() + \
		   open(root + "/html/2_pick_location.html", "r").read() + \
		   open(root + "/html/3_results.html", "r").read() + \
		   open(root + "/html/footer.html", "r").read()
	return text

@post('/request_render')
def request_render():
	print(request.files.__dict__)
	time.sleep(5)

#----------------------- Serve files


@route('/favicon')
def favicon():
	return static_file("favicon.jpeg", root="/Users/2017-A/Dropbox/web_dev/modelcraft")

@route('/show_layout_pdf/<session_id>')
def serve_layout_pdf(session_id):
	return static_file("layout.pdf", root="/Users/2017-A/Dropbox/web_dev/modelcraft")

@route('/show_cutout_pdf/<session_id>')
def serve_layout_pdf(session_id):
	return static_file("layout.pdf", root="/Users/2017-A/Dropbox/web_dev/modelcraft")

@route('/download_layout_pdf/<session_id>')
def serve_layout_pdf(session_id):
	return static_file("layout.pdf", root="/Users/2017-A/Dropbox/web_dev/modelcraft/data/" + session_id, download="layout.pdf")

@route("/download_dxf/<session_id>")
def dxf(session_id):
	return static_file("cutout.dxf", root="/Users/2017-A/Dropbox/web_dev/modelcraft/data/"+session_id, download="cutout.dxf")

@route('/get_stylesheet')
def stylesheet():
	return static_file("stylesheet.css", root="/Users/2017-A/Dropbox/web_dev/modelcraft/css")

@route('/javascript_functions')
def stylesheet():
	return static_file("script.js", root="/Users/2017-A/Dropbox/web_dev/modelcraft/javascript")

@route('/serve_icon/<session_id>')
def serve_icon(session_id):
	return static_file("icon.png", root="/Users/2017-A/Dropbox/web_dev/modelcraft/data/" + session_id + "/map")

@route('/root_image')
def root_image():
	return static_file("house.jpeg", root="/Users/2017-A/Dropbox/web_dev/modelcraft")


try:
	run(host='0.0.0.0', port=80, debug=True)
except:
	run(host='localhost', port=8080, debug=True)