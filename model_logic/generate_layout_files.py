def generate_layout_files(root_path, session_id, block_array, type=["pdf"]):
    image_paths = generate_layout_images(root_path, session_id, block_array)
    down = max(color_array.shape[0], color_array.shape[1])
    across = min(color_array.shape[0], color_array.shape[1])
    generate_layout_pdf(image_paths)

def generate_layout_images(root_path, session_id, block_array):
    folder_path = root_path + "/data/" + session_id + "/layout_images"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)

    image_names = []
    for z in range(color_array.shape[2]):
        data = draw_level(10, color_array[:, :, z])
        img = Image.fromarray(data, 'RGB')
        img_name = folder_path + "/" + str(z) + ".png"
        image_names.append(img_name)
        img.save(img_name)

    return image_names

def generate_layout_pdf(image_paths):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(root_path + "/front_page.jpeg", 5, 0, 200, 275)
    # imagelist is the list with all image filenames
    down = max(color_array.shape[0], color_array.shape[1])
    across = min(color_array.shape[0], color_array.shape[1])
    for image in image_names:
        pdf.add_page()
        pdf.image(image, 5, 5, 250 / 70 * across, 250 / 70 * down)
    pdf.output(root_path + "/data/" + session_id + "/layout.pdf", "F")
