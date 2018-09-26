"use strict";
function jump_to(path) {
    if (navigator.userAgent.match(/Chrome|AppleWebKit/)) {
        window.location.href = "#" + path;
        window.location.href = "#" + path;  /* these take twice */
    } else {
        window.location.hash = path;
    }
}

function check_step_1() {
    return true;
}

function step_1_reprompt() {}

function check_step_2() {
    return true;
}

function step_2_reprompt() {}

function start_process() {
    jump_to("upload_map");
}

function finish_step_1() {
    if (!check_step_1()) {
        step_1_reprompt();
    } else {
        jump_to("pick_location");
    }
}

function finish_step_2() {
    console.log("finish step 2?");
    if (!check_step_2()) {
        step_2_reprompt();
    } else {
        render_results();
    }
    return false;
}

function request_render(session_id_file, level_dat_file, region_files, position_file) {
    var form_data = new FormData();
    form_data.set('session_id_file', level_dat_file);
    form_data.set('level_dat', level_dat_file);
    form_data.set('position', position_file);
    for (let i=0; i<region_files.length; i++) {
        form_data.set(i.toString(), region_files[i]);
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             display_results();
         }
    };
    xhttp.open("POST", "/request_render", true);
    xhttp.send(form_data);
}

function render_results() {
    document.getElementById("no_results").style.display = "none";
    document.getElementById("loading_bar").style.display = "block";

    let session_id = document.getElementById("session_id").value.toString();
    let session_id_file = new File([session_id],
        "position.txt", {type: "text/plain",});

    let x1 = document.getElementById("x1").value.toString();
    let y1 = document.getElementById("y1").value.toString();
    let z1 = document.getElementById("z1").value.toString();
    let x2 = document.getElementById("x2").value.toString();
    let y2 = document.getElementById("y2").value.toString();
    let z2 = document.getElementById("z2").value.toString();

    let position_file = new File([x1 + " " + y1 + " " + z1 + " " + x2 + " " + y2 + " " + z2],
        "position.txt", {type: "text/plain",});

    var level_dat_file = document.getElementById("level_dat").files[0];
    var region_files = document.getElementById("region").files;

    request_render(session_id_file, level_dat_file, region_files, position_file);
}

function display_results() {
    document.getElementById("loading_bar").style.display = "none";
    document.getElementById("show_results").style.display = "block";
}