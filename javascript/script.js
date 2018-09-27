"use strict";

function show_error_message(location, message) {
    document.getElementById(location + "_error_div").style.display = "block";
    document.getElementById(location + "_error_p").innerHTML = message;
}

function hide_error_message(location) {
    document.getElementById(location + "_error_div").style.display = "none";
}

function jump_to(path) {
    if (navigator.userAgent.match(/Chrome|AppleWebKit/)) {
        window.location.href = "#" + path;
        window.location.href = "#" + path;  /* these take twice */
    } else {
        window.location.hash = path;
    }
}

function check_step_1() {
    var level_dat_files = document.getElementById("level_dat").files;
    var region_files = document.getElementById("region").files;
    if (level_dat_files.length == 0) {
        return "level.dat file missing";
    } else if (region_files.length == 0) {
        return "region files missing";
    }
    return "good";
}

function check_step_2() {
    let must_be_ints = ["x1", "y1", "z1", "x2", "y2", "z2"];
    let error_text = "";
    for (let i=0; i<must_be_ints.length; i++) {
        let val = parseInt(document.getElementById(must_be_ints[i]).value);
        if (isNaN(val)) {
            error_text += must_be_ints[i] + " is missing\n";
        }
    }
    if (error_text == "") {
        return "good";
    } else {
        return error_text;
    }
}

function start_process() {
    jump_to("upload_map");
}

function finish_step_1() {
    let step_1_status = check_step_1();
    if (!(step_1_status == "good")) {
        show_error_message("upload_map", step_1_status);
        jump_to("find_your_map");
        return;
    }

    hide_error_message("upload_map");
    jump_to("pick_location");
}

function finish_step_2() {
    let step_2_status = check_step_2();
    if (!(step_2_status == "good")) {
        show_error_message("pick_location", step_2_status);
        jump_to("select_corners");
        return;
    }

    let step_1_status = check_step_1();
    if (!(step_1_status == "good")) {
        show_error_message("upload_map", step_1_status);
        jump_to("find_your_map");
        return;
    }

    hide_error_message("upload_map");
    hide_error_message("pick_location");

    render_results();
}

function request_render(session_id_file, level_dat_file, region_files, position_file) {
    let form_data = new FormData();
    form_data.set('session_id', session_id_file);
    form_data.set('level_dat', level_dat_file);
    form_data.set('position', position_file);
    for (let i=0; i<region_files.length; i++) {
        form_data.set(i.toString(), region_files[i]);
    }

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             display_results();
         }
    };
    xhttp.open("POST", "/request_render", true);
    xhttp.send(form_data);
}

function render_results() {
    document.getElementById("no_results_laser_cut").style.display = "none";
    document.getElementById("loading_bar_build").style.display = "block";
    document.getElementById("show_results_build").style.display = "none";

    document.getElementById("no_results_build").style.display = "none";
    document.getElementById("loading_bar_build").style.display = "block";
    document.getElementById("show_results_build").style.display = "none";

    let session_id = document.getElementById("session_id").value.toString();
    var session_id_file = new File([session_id],
        "session_id.txt", {type: "text/plain",});

    let x1 = document.getElementById("x1").value;
    let x2 = document.getElementById("x2").value;
    let y1 = document.getElementById("y1").value;
    let y2 = document.getElementById("y2").value;
    let z1 = document.getElementById("z1").value;
    let z2 = document.getElementById("z2").value;

    document.getElementById("layout_image_largest_value").value = Math.abs(z1-z2)-1;

    let num_text = x1 + " " + y1 + " " + z1 + " " + x2 + " " + y2 + " " + z2;

    let position_file = new File([num_text],
        "position.txt", {type: "text/plain",});

    let level_dat_file = document.getElementById("level_dat").files[0];
    let region_files = document.getElementById("region").files;

    request_render(session_id_file, level_dat_file, region_files, position_file);
    return session_id_file;
}

function load_layout_image(position) {
    let session_id = document.getElementById("session_id").value.toString();
    document.getElementById("layout_image").src =
        "/layout_image/" + session_id + "/" + position.toString();
}

function layout_image_change(change) {
    let current_location_form = document.getElementById("layout_image_current_location");
    let current_location_int = parseInt("0" + current_location_form.value);
    let max_value = parseInt(document.getElementById("layout_image_largest_value").value);
    current_location_int += change;
    if (current_location_int < 0) {
        current_location_int = max_value;
    } else if (current_location_int > max_value) {
        current_location_int = 0;
    }

    current_location_form.value = current_location_int.toString();
    load_layout_image(current_location_int);
}

function display_results() {
    document.getElementById("no_results_laser_cut").style.display = "none";
    document.getElementById("loading_bar_laser_cut").style.display = "none";
    document.getElementById("show_results_laser_cut").style.display = "block";
    load_layout_image(0);

    document.getElementById("no_results_build").style.display = "none";
    document.getElementById("loading_bar_build").style.display = "none";
    document.getElementById("show_results_build").style.display = "block";
}