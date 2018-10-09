import time
import datetime
import os


def log_unsuccessful_login(root_path, request):
    log_admin_activity(root_path, "UNSUCCESSFUL LOGIN", request)


def log_successful_login(root_path, request):
    log_admin_activity(root_path, "Successful login", request)


def log_admin_activity(root_path, activity, request):
    admin_log = open(root_path + "/secret_data/admin_log.txt", "a")
    timestamp = datetime.datetime.fromtimestamp(time.time())\
        .strftime('%Y-%m-%d %H:%M:%S')
    admin_log.write(timestamp + " " + request.environ.get('REMOTE_ADDR') + " " + activity + "\n")
    admin_log.close()


def get_all_session_infos(root_path, request):
    log_admin_activity(root_path, "get all session ids", request)
    session_ids = os.listdir(root_path + "/data")
    session_ids = filter(lambda x: x[0] != '.', session_ids)
    session_infos = [session_id + "\n" + open(root_path + "/data/" + session_id + "/session_info.txt").read() for session_id in session_ids]

    return session_infos

