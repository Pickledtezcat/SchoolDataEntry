import json
import os

from PIL import Image


def save_file(content, file_name):
    out_path = "{}{}.js".format(get_path(), file_name)

    with open(out_path, "w") as outfile:
        converted_content = json.dumps(content, sort_keys=True)
        outfile.write("window.{} ={}".format(file_name, converted_content))


def load_file(file_name):
    in_path = "{}{}.js".format(get_path(), file_name)

    with open(in_path, "r") as infile:
        loaded_content = infile.read()
        if len(loaded_content) > 0:
            converted_content = loaded_content.split("=")[1]
            content = json.loads(converted_content)
            return content
        else:
            return None


def get_path():
    path = "D:/projects//gitpages//numlocked//Pickledtezcat.github.io//"
    return path


def strip_name(file_name):
    type_removed = file_name.lower().split(".")[0]

    split_name = type_removed.split("_")
    part_list = []

    for word in split_name:
        parts = "".join([i for i in word if not i.isdigit() and i != "-"])
        if parts != "":
            print(parts)
            part_list.append(parts)

    stripped_name = "_".join(part_list)
    second_split = stripped_name.split(" ")
    valid_parts = [section for section in second_split if len(section) > 0]

    final_spilt = " ".join(valid_parts)

    return final_spilt


def get_image_list():
    main_path = "{}pictures//".format(get_path())
    origin_path = "{}origin_files//".format(main_path)

    processing = []
    save_list = []

    for path, dirs, files in os.walk(origin_path):

        for file_name in files:

            stripped_name = strip_name(file_name)
            count = 1
            for used in save_list:
                if used == stripped_name:
                    count += 1

            new_name = "{}_{}".format(stripped_name, count)
            image_path = "{}{}".format(origin_path, file_name)

            save_list.append(stripped_name)
            processing.append([image_path, new_name])

    return save_list, processing


def process_image(image_path, new_name):
    cell_size = 600
    main_path = "{}pictures//".format(get_path())

    with Image.open(image_path, "r") as im:
        bbox = im.getbbox()

        x_size = bbox[2]
        y_size = bbox[3]

        multi = 1.0 / float(cell_size)

        scaler = float(y_size) * multi

        y_target = cell_size
        x_target = int(x_size / scaler)

        im = im.convert("RGB")
        im = im.resize((x_target, y_target), Image.ANTIALIAS)

        save_name = "{}{}.jpeg".format(main_path, new_name)
        im.save(save_name, "jpeg", quality=60, )


def process_images_x():
    cell_size = 600

    main_path = "{}pictures//".format(get_path())
    origin_path = "{}origin_files//".format(main_path)

    processed = []

    for path, dirs, files in os.walk(origin_path):

        for file_name in files:

            stripped_name = strip_name(file_name)
            count = 1
            for used in processed:
                if used == stripped_name:
                    count += 1

            new_name = "{}_{}".format(stripped_name, count)

            processed.append(stripped_name)

            image_path = "{}{}".format(origin_path, file_name)

            with Image.open(image_path, "r") as im:

                bbox = im.getbbox()

                x_size = bbox[2]
                y_size = bbox[3]

                multi = 1.0 / float(cell_size)

                scaler = float(y_size) * multi

                y_target = cell_size
                x_target = int(x_size / scaler)

                im = im.convert("RGB")
                im = im.resize((x_target, y_target), Image.ANTIALIAS)

                save_name = "{}{}.jpeg".format(main_path, new_name)
                print(save_name)

                im.save(save_name, "jpeg", quality=60,)

    return processed
