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

// When the user scrolls the page, execute myFunction 
window.onscroll = function() {stickyHeader()};

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyHeader() {
    // Get the header
    var header = document.getElementById("div1");

    // Get the offset position of the navbar
    var sticky = header.offsetTop;
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
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
    jump_to("jump1");
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

function request_render(session_id_file, level_dat_file, region_files, position_file, settings_file) {
    let form_data = new FormData();
    form_data.set('session_id', session_id_file);
    form_data.set('level_dat', level_dat_file);
    form_data.set('position', position_file);
    form_data.set('settings', settings_file);
    for (let i=0; i<region_files.length; i++) {
        form_data.set(i.toString(), region_files[i]);
    }

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             console.log("Thread started");
             let laser_cut_load_text = document.getElementById("loading_text_laser_cut");
             let layout_load_text = document.getElementById("loading_text_layout");
             laser_cut_load_text.innerHTML = "Requesting render";
             layout_load_text.innerHTML = "Requesting render";
             wait_for_render();
         }
    };
    xhttp.open("POST", "/request_render", true);
    xhttp.send(form_data);
}

function get_radio_value(name) {
    var radios = document.getElementsByName(name);

    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            // do whatever you want with the checked radio
            return(radios[i].value);
        }
    }
}

function render_results() {
    document.getElementById("no_results_laser_cut").style.display = "none";
    document.getElementById("loading_laser_cut").style.display = "block";
    document.getElementById("show_results_laser_cut").style.display = "none";

    document.getElementById("no_results_layout").style.display = "none";
    document.getElementById("loading_layout").style.display = "block";
    document.getElementById("show_results_layout").style.display = "none";

    var session_id_file = new File([get_session_id()],
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

    let hollow = get_radio_value("hollow");
    let supports = get_radio_value("add_supports");

    let width = document.getElementById("width").value;
    let length = document.getElementById("length").value;
    let thickness = document.getElementById("thickness").value;
    let tab_size = document.getElementById("tab_size").value;
    let piece_size = document.getElementById("piece_size").value;

    let water = get_radio_value("water_settings");
    let lava = get_radio_value("lava_settings");
    let clear = get_radio_value("clear_settings");
    let fence = get_radio_value("fence_settings");
    let torch = get_radio_value("torch_settings");
    let ladder = get_radio_value("ladder_settings");


    let settings_text = hollow + " " + supports + "\n";
    settings_text += width + " " + length + " " + thickness + " " + tab_size + " " + piece_size + "\n";
    settings_text += water + " " + lava + " " + clear + " " + fence + " " + torch + " " + ladder;

    let settings_file = new File([settings_text],
        "settings.txt", {type: "text/plain",});

    let level_dat_file = document.getElementById("level_dat").files[0];
    let region_files = document.getElementById("region").files;

    request_render(session_id_file, level_dat_file, region_files, position_file, settings_file);
    return session_id_file;
}

function reload_layout_images() {
    let image_div = document.getElementById("layout_images");
    image_div.innerHTML = "";
    let max_value = parseInt(document.getElementById("layout_image_largest_value").value);
    let newImg;
    for (let i=0; i<=max_value; i++) {
        newImg = document.createElement("img");
        newImg.src = "/layout_image/" + get_session_id() + "/" + i.toString() + "/" + cache_breaker();
        newImg.className = "layout_image";
        image_div.appendChild(newImg);
    }
}

function get_session_id() {
    return document.getElementById("session_id").value.toString();
}


function display_layout_results() {
    reload_layout_images();
    document.getElementById("no_results_layout").style.display = "none";
    document.getElementById("loading_layout").style.display = "none";
    document.getElementById("show_results_layout").style.display = "block";
}

function display_laser_cut_results() {
    reload_cutout_images();
    document.getElementById("no_results_laser_cut").style.display = "none";
    document.getElementById("loading_laser_cut").style.display = "none";
    document.getElementById("show_results_laser_cut").style.display = "block";
}

function cache_breaker() {
    return new Date().getTime();
}

function toggle_advanced_settings() {
    let settings = document.getElementById("advanced_settings");
    if (settings.style.display === "none") {
        settings.style.display = "block";
    } else {
        settings.style.display = "none";
    }
}

function render_color_section(color_id) {
    let location = document.getElementById("cutout_images");
    let new_div = document.createElement('div');
    new_div.className = "color_section";
    new_div.id = "color_" + color_id.toString();
    location.appendChild(new_div);

    let title = document.createElement('h1');
    if (color_id.toString() == "other") {
        title.appendChild(document.createTextNode("main"));
    } else {
        title.appendChild(document.createTextNode(color_id.toString()));
    }
    new_div.appendChild(title);
}

function render_sheet(color_id, sheet_id) {
    let div = document.getElementById("color_" + color_id.toString());
    let new_image = document.createElement('img');
    new_image.src = "/cutout_image/" + get_session_id() + "/" + color_id.toString() + "/" + sheet_id.toString() + "/" + cache_breaker();
    div.appendChild(new_image);
}

function render_download_dxf_button(color) {
    let location = document.getElementById("color_" + color);

    let new_div = document.createElement('div');
    new_div.id = "buttons";
    location.appendChild(new_div);

    let form = document.createElement('form');
    form.action = "/download_laser_cut_dxf/" + get_session_id() + "/" + color;
    form.target = "_blank";
    new_div.appendChild(form);

    let input = document.createElement('input');
    input.id="download_dxf_input_" + color;
    input.type="submit";
    input.value="Download as dxf";
    form.appendChild(input);
    /*
    <div id="buttons">
        <form action="/download_laser_cut_dxf/$$session_id$$" target="_blank">
            <input id="download_dxf_input" type="submit" value="Download as dxf" style="display: none"/>
        </form>
        <label for="download_dxf_input" style="padding: 1em">Download as dxf</label>
    </div>
    */
}


function reload_cutout_images() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            let cutout_info = JSON.parse(xmlHttp.responseText);
            let iter1, iter2, color, sheet;
            let location = document.getElementById("cutout_images");
            location.innerHTML = "";
            console.log(cutout_info);
            for (iter1 in Object.keys(cutout_info.data)) {
                color = Object.keys(cutout_info.data)[iter1];
                render_color_section(color);
                console.log(color);
                var cutout = cutout_info;
                console.log(cutout_info.data[color]);
                for (iter2 in cutout_info.data[color]) {
                    sheet = cutout_info.data[color][iter2];
                    console.log("Rendering sheet");
                    render_sheet(color, sheet);
                }
                render_download_dxf_button(color);
            }
        }
    }
    xmlHttp.open("GET", "/available_cutouts/" + get_session_id() + "/" + cache_breaker(), true); // true for asynchronous
    xmlHttp.send(null);
}

var stop = false;
function wait_for_render() {
    let update_load_bar = setTimeout(function tick() {
        console.log('tick');
        if (stop) {
            return;
        }

        let laser_cut_loading = document.getElementById("loading_laser_cut");
        if (laser_cut_loading.style.display == "block") {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    let state = xmlHttp.responseText.split("\n");
                    console.log(state);
                    let state_text = state[0];
                    let state_load = parseInt(state[1]);
                    if (state_load > 20) {
                        let layout_display = document.getElementById("show_results_layout");
                        if (layout_display.style.display != "block") {
                            display_layout_results();
                        }
                    }
                    if (state_load == 100) {
                        display_laser_cut_results();
                        return;
                    }
                    let laser_cut_bar = document.getElementById("loading_bar_laser_cut");
                    let layout_bar = document.getElementById("loading_bar_layout");
                    laser_cut_bar.style.width = state_load.toString() + "%";
                    layout_bar.style.width = state_load.toString() + "%";
                    let laser_cut_load_text = document.getElementById("loading_text_laser_cut");
                    let layout_load_text = document.getElementById("loading_text_layout");
                    laser_cut_load_text.innerHTML = state_text;
                    layout_load_text.innerHTML = state_text;
                }
            }
            xmlHttp.open("GET", "/render_state/" + get_session_id() + "/" + cache_breaker(), true); // true for asynchronous
            xmlHttp.send(null);

            update_load_bar = setTimeout(tick, 2000); // (*)
        }
    }, 2000);
}