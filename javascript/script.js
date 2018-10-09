"use strict";

document.body.scrollTop = document.documentElement.scrollTop = 0;

function show_available_models() {
    document.getElementById("available_models_div").style.display = "block";

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            let outer = document.getElementById("models");
            outer.innerHTML = "";
            let models = xmlHttp.responseText.split("\n");
            for (let i=0; i<models.length; i++) {
                console.log(models[i]);
                add_model(models[i].split("%%%"));
            }
        }
    }
    xmlHttp.open("GET", "/available_models", true); // true for asynchronous
    xmlHttp.send(null);
}

function add_model(model_info) {
    let model_id = model_info[0];
    let model_name = model_info[1];
    let model_description = model_info[2];
    let outer = document.getElementById("models");

    let container = document.createElement("div");
    container.className = "model_div";
    outer.appendChild(container);

    let left_side = document.createElement("div");
    left_side.className = "left_side";
    container.appendChild(left_side);

    let newImg = document.createElement("img");
    newImg.src = "/model_icon/" + model_id;
    newImg.className = "model_icon";
    left_side.appendChild(newImg);

    let right_side = document.createElement("div");
    right_side.className = "right_side";
    container.appendChild(right_side);

    let title = document.createElement('h1');
    title.appendChild(document.createTextNode(model_name));
    right_side.appendChild(title);

    let description = document.createElement('p');
    description.appendChild(document.createTextNode(model_description));
    right_side.appendChild(description);

    let buttons_div = document.createElement("div");
    newImg.className = "buttons_div";
    right_side.appendChild(buttons_div);

    let buttons = document.createElement("div");
    buttons.className = "model_buttons";

    let form = document.createElement("form");
    form.action = "/download_model_laser_cut_dxf/" + model_id;
    form.target = "_blank";
    let input = document.createElement("input");
    input.type = "submit";
    input.style = "display: none";
    input.id = "download_model_dxf_" + model_id;
    form.appendChild(input);
    buttons.appendChild(form);
    let label = document.createElement("label");
    label.htmlFor = "download_model_dxf_" + model_id;
    label.appendChild(document.createTextNode("Cutout\n(.dxf)"));
    buttons.appendChild(label);

    let form_right = document.createElement("form");
    form_right.action = "/download_model_layout_pdf/" + model_id;
    form_right.target = "_blank";
    let input_right = document.createElement("input");
    input_right.type = "submit";
    input_right.style = "display: none";
    input_right.id = "download_model_pdf_" + model_id;
    form_right.appendChild(input_right);
    buttons.appendChild(form_right);
    let label_right = document.createElement("label");
    label_right.htmlFor = "download_model_pdf_" + model_id;
    label_right.appendChild(document.createTextNode("Layout\n(.pdf)"));
    buttons.appendChild(label_right);

    container.append(buttons);
}

function hide_available_models() {
    document.getElementById("available_models_div").style.display = "none";
}

function show_landing_page() {
    document.getElementById("description_div").style.display = "block";
}

function hide_landing_page() {
    document.getElementById("description_div").style.display = "none";
}

function show_make_your_own() {
    document.getElementById("upload_map_div").style.display = "block";
    document.getElementById("pick_location_div").style.display = "block";
    document.getElementById("laser_cut_div").style.display = "block";
    document.getElementById("build_div").style.display = "block";
    document.getElementById("advanced_settings_div").style.display = "block";
    document.getElementById("jump1").style.display = "block";
    document.getElementById("jump2").style.display = "block";
    document.getElementById("jump3").style.display = "block";
}

function hide_make_your_own() {
    document.getElementById("upload_map_div").style.display = "none";
    document.getElementById("pick_location_div").style.display = "none";
    document.getElementById("laser_cut_div").style.display = "none";
    document.getElementById("build_div").style.display = "none";
    document.getElementById("advanced_settings_div").style.display = "none";
    document.getElementById("jump1").style.display = "none";
    document.getElementById("jump2").style.display = "none";
    document.getElementById("jump3").style.display = "none";
}

function click_make_your_own() {
    hide_available_models();
    hide_landing_page();
    show_make_your_own();
    jump_to("behind_header");
}

function click_available_models() {
    hide_make_your_own();
    hide_landing_page();
    show_available_models();
    jump_to("behind_header");
}

function click_landing_page() {
    hide_make_your_own();
    hide_available_models();
    show_landing_page();
    jump_to("behind_header");
}

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

// When the user scrolls the page, execute stickyHeader 
window.onscroll = function() {stickyHeader()};

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyHeader() {
    // Get the header
    var header = document.getElementById("buffer_div");

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
        jump_to("jump1");
        return;
    }

    hide_error_message("upload_map");
    jump_to("jump2");
}

function finish_step_2() {
    let step_2_status = check_step_2();
    if (!(step_2_status == "good")) {
        show_error_message("pick_location", step_2_status);
        jump_to("jump2");
        return;
    }

    let step_1_status = check_step_1();
    if (!(step_1_status == "good")) {
        show_error_message("upload_map", step_1_status);
        jump_to("jump1");
        return;
    }

    hide_error_message("upload_map");
    jump_to("jump3");

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