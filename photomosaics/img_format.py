from PIL import Image


def crop_to_square(image, path):
    if image.size[0] == image.size[1]:
        image.save(path)
    else:
        if image.size[0] > image.size[1]:
            cropped = image.crop((0, 0, image.size[1], image.size[1]))
            cropped.save(path)
        else:
            cropped = image.crop((0, 0,image.size[0], image.size[0]))
            cropped.save(path)


def process_to_square(src_path, path, image_number):
    for i in range(0, image_number):
        if i < 10:
            temp_img = Image.open("{}/person_000{}.jpg".format(src_path, i))
        elif i >= 100:
            temp_img = Image.open("{}/person_0{}.jpg".format(src_path, i))
        else:
            temp_img = Image.open("{}/person_00{}.jpg".format(src_path, i))
        save_path = path + "/" + str(i) + ".jpg"
        crop_to_square(temp_img, save_path)


if __name__ == "__main__":
    source_path = input("Please enter the source directory path: ")
    created_path = input("Please enter a name for new source directory path: ")
    number = input("Please enter the number of images you want to use: ")
    process_to_square(source_path, created_path, int(number))

