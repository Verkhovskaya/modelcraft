"use strict";

function list_sessions() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            let session_infos = xmlHttp.responseText.split("%%%");
            console.log(session_infos);
            for (let i = 0; i < session_infos.length; i++) {
                list_session(session_infos[i].split("\n"));
            }
        }
    }
    xmlHttp.open("GET", "/admin/session_infos", true); // true for asynchronous
    xmlHttp.send(null);
}

function list_session(session_info) {
    let session_id = session_info[0];
    let session_timestamp = session_info[1];
    let session_ip_address = session_info[2];

    let sessions_screen = document.getElementById("admin_sessions_screen");
    let session_div = document.createElement("div");

    sessions_screen.appendChild(session_div);

    let title = document.createElement("p");
    title.innerHTML = session_id;
    session_div.appendChild(title);

    let timestamp = document.createElement("p");
    timestamp.innerHTML = session_timestamp;
    session_div.appendChild(timestamp);

    let ip_address = document.createElement("p");
    ip_address.innerHTML = session_ip_address;
    session_div.appendChild(ip_address);

    let form_dxf = document.createElement("form");
    form_dxf.action = "/admin/cutout_dxf/" + session_id;
    form_dxf.target = "_blank";
    let input_dxf = document.createElement("input");
    input_dxf.type = "submit";
    input_dxf.innerHTML = "DXF";
    form_dxf.appendChild(input_dxf);
    session_div.appendChild(form_dxf);

    let form_pdf = document.createElement("form");
    form_pdf.action = "/admin/layout_pdf/" + session_id;
    form_pdf.target = "_blank";
    let input_pdf = document.createElement("input");
    input_pdf.type = "submit";
    input_pdf.innerHTML = "PDF";
    form_pdf.appendChild(input_pdf);
    session_div.appendChild(form_pdf);

    let form_log_txt = document.createElement("form");
    form_log_txt.action = "/admin/log_txt/" + session_id;
    form_log_txt.target = "_blank";
    let input_log_txt = document.createElement("input");
    input_log_txt.type = "submit";
    input_log_txt.innerHTML = "PDF";
    form_log_txt.appendChild(input_log_txt);
    session_div.appendChild(form_log_txt);
}

window.onload = function() {
    list_sessions();
};
