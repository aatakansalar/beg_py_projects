from PIL import Image
import numpy as np
import copy
import math
import json

"""
Use img_format.py first if your source images are not all square images
TODO: Optimization with pre-calculation and increasing the detail in photo matching
"""


def crop_to_pieces(image, piece_height, piece_width):
    img_width, img_height, count = image.size[0], image.size[1], 0
    for i in range(0, img_height, piece_height):
        for j in range(0, img_width, piece_width):
            box = (j, i, j + piece_height, i + piece_width)
            piece, count = image.crop(box), count + 1
            piece.save("piece_%s.jpg" % count)


def to_piece(img_arr, p_height, p_width):
    pieces = list()
    for i in range(0, img_arr.shape[0], p_height):
        for j in range(0, img_arr.shape[1], p_width):
            piece = img_arr[i:i+p_height, j:j+p_width]
            pieces.append(piece)
    return pieces


def rgb_avg(obj_input, input_type):
    sum_r, sum_g, sum_b = 0, 0, 0
    if input_type == "image":
        arr = np.asarray(obj_input)
    else:
        arr = obj_input
    img_h, img_w = len(arr), len(arr[0])
    for i in range(0, img_h):
        for j in range(0, img_w):
            sum_r += arr[i][j][0]
            sum_g += arr[i][j][1]
            sum_b += arr[i][j][2]
    avg_r, avg_g, avg_b = sum_r // (img_h * img_w), sum_g // (img_h * img_w), sum_b // (img_h * img_w)
    return [avg_r, avg_g, avg_b]


def euclidean_distance_rgb(p_avg, i_avg):
    sub_r, sub_g, sub_b = p_avg[0] - i_avg[0], p_avg[1] - i_avg[1], p_avg[2] - i_avg[2]
    distance = math.sqrt(sub_r ** 2 + sub_g ** 2 + sub_b ** 2)
    return distance


def src_img_avgs(src_path, image_number):
    arr = []
    for i in range(0, image_number):
        path = "{}/{}.jpg".format(src_path, i)
        # temp_img = Image.open(path)
        rgb_average = find_cached_avg('mean_rgb_cache.json', path)
        arr.append([path, rgb_average])
    return arr


def pixellate(image, scale_y, scale_x, path):
    img_arr = np.asarray(image)
    new_img_arr = copy.deepcopy(img_arr)
    pieces, m = to_piece(img_arr, scale_y, scale_x), 0
    for i in range(0, new_img_arr.shape[0], scale_y):
        for j in range(0, new_img_arr.shape[1], scale_x):
            color = rgb_avg(pieces[m], "piece")
            m += 1
            new_img_arr[i:i + scale_y, j:j + scale_x] = color
    img = Image.fromarray(new_img_arr, "RGB")
    img.save(path)


def match_piece_to_image(pieces, src_img_avgs_arr):
    matches = []
    for k in range(0, len(pieces)):
        temp_piece_avg = rgb_avg(pieces[k], "piece")
        temp_dist_arr = []
        for i in range(0, len(src_img_avgs_arr)):
            temp_dist_arr.append(math.ceil(euclidean_distance_rgb(temp_piece_avg, src_img_avgs_arr[i][1])))
        min_distance_index = temp_dist_arr.index(min(temp_dist_arr))
        matches.append([src_img_avgs_arr[min_distance_index][0]])
    return matches


def match_to_image(image, scale_y, scale_x, src_path, image_number, create_path):
    img_arr, piece_count = np.asarray(image), 0
    new_img_arr = copy.deepcopy(img_arr)
    pieces = to_piece(img_arr, scale_y, scale_x)
    src_img_averages_arr = src_img_avgs(src_path, image_number)
    matches = match_piece_to_image(pieces, src_img_averages_arr)
    for i in range(0, img_arr.shape[0], scale_y):
        for j in range(0, img_arr.shape[1], scale_x):
            temp_img = Image.open(matches[piece_count][0])
            size = (scale_y, scale_x)
            resized_temp_img = temp_img.resize(size)
            resized_temp_img_arr = np.asarray(resized_temp_img)
            new_img_arr[i:i + scale_y, j:j + scale_x] = resized_temp_img_arr
            piece_count += 1
    img = Image.fromarray(new_img_arr, "RGB")
    img.save(create_path)


def write_json(data, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def cache_avg(filename, key, average):
    with open(filename) as json_file:
        data = json.load(json_file)
        temp = data['avg_rgb']
        avg_str = str(average[0]) + "," + str(average[1]) + "," + str(average[2])
        avg = {key: avg_str}
        temp.append(avg)
    write_json(data, filename)


def find_cached_avg(filename, key):
    with open(filename) as json_file:
        data = json.load(json_file)
        for i in range(0, len(data['avg_rgb'])):
            if key in data['avg_rgb'][i]:
                avg = data['avg_rgb'][i][key]
                avg_arr = avg.split(',')
                avg_arr[0], avg_arr[1], avg_arr[2] = int(avg_arr[0]), int(avg_arr[1]), int(avg_arr[2])
                return avg_arr
    temp_img = Image.open(key)
    avg = rgb_avg(temp_img, "image")
    cache_avg(filename, key, avg)
    return avg


if __name__ == "__main__":
    # USER INPUTS
    image_name = input("Please enter the image name/path: ")
    scale_x, scale_y = int(input("Please enter scale_x: ")), int(input("Please enter scale_y: "))
    source_path = input("Please enter path to source photos directory: ")
    image_number = int(input("Please enter the number of source photos you want to use: "))
    name_of_new_img = input("Please enter a name for created file: ")

    image = Image.open(image_name, "r")
    if image.size[0] % scale_x or image.size[1] % scale_y:
        x_t, y_t = image.size[0] // scale_x, image.size[1] // scale_y
        resized_img = image.resize((x_t*scale_x, y_t*scale_y))
        match_to_image(resized_img, scale_x, scale_y, source_path, image_number, name_of_new_img)
    else:
        match_to_image(image, scale_x, scale_y, source_path, image_number, name_of_new_img)
