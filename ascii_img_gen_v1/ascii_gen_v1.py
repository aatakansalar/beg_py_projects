from PIL import Image
import numpy as np
import sys
import math as mt
from colorama import init, deinit, Fore

"""
USE INSTRUCTIONS
>> python ascii_gen_v1.py "avg" "final.jpg" "r" 24
Method options: "lum" "avg" "light"
Color Options: "r"(regular output) "red" "green" "blue" "dark"
Dark mode inverts the brightness of the ascii output
Resize: for small images, 2 or 4 is enough, for larger ones 8 seems ideal
"""

# Starting colorama for color options
init()
# A variable for resizing the image proportionally
resize_scale = 4
filepath = sys.argv[2]


# A function that takes the calculated average (by whatever method that was used)
# and returns the correspondent character from our string ascii
def to_char(str, avg):
    weight = light_dark(sys.argv[3], avg) / 255
    result = mt.ceil(len(str) * weight)
    if result == 0:
        return str[result]
    else:
        return str[result - 1]


# Calculates and returns the basic average of RGB values of a pixel
def to_avg(string, tuple):
    avg = (int(tuple[0]) + int(tuple[1]) + int(tuple[2])) / 3
    return to_char(string, avg)


# Calculates and returns the average of RGB values by min+max/2 method
def to_lightness(string, tuple):
    maxi = max(tuple[0], tuple[1], tuple[2])
    mini = min(tuple[0], tuple[1], tuple[2])
    avg = (maxi + mini) // 2
    return to_char(string, avg)


# Calculates and returns the weighted average of RGB values of a pixel by
# Weight values are based on the eyes perception to red, blue or green respectively
def to_luminosity(string, tuple):
    avg = (0.21 * tuple[0] + 0.72 * tuple[1] + 0.07 * tuple[2]) // 2
    return to_char(string, avg)


# Print function, can print r,b or g text with colorama with s parameter
# If no parameter is entered, default is used
def asc_print(s, char):
    if s == "red":
        print(Fore.RED, char, char, end="")
    elif s == "green":
        print(Fore.GREEN, char, char, end="")
    elif s == "blue":
        print(Fore.BLUE, char, char, end="")
    elif s == "r":
        print(char, char,  end="")


# If user enters "dark" as a command line argument, we switch the characters
# So the bolder characters are used for opposite reasons etc.
def light_dark(s, input):
    if s == "dark":
        return 255 - input
    else:
        return input


# Character string from https://robertheaton.com/2018/06/12/programming-projects-for-advanced-beginners-ascii-art/
ascii = '`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

# Opening th image
img = Image.open(filepath)

# Resizing the image to make it easier to process and observe
img_resized = img.resize((img.size[0] // resize_scale, img.size[1] // resize_scale), Image.ANTIALIAS)

# We get the pixels as a numpy matrix
img_arr = np.asarray(img_resized)


if sys.argv[1] == "avg":
    print("avg")
    for x in range(0, len(img_arr)):
        print("\n", end="")
        for y in range(0, len(img_arr[x])):
            char = to_avg(ascii, img_arr[x][y])
            asc_print(sys.argv[3], char)

elif sys.argv[1] == "light":
    print("light")
    for x in range(0, len(img_arr)):
        print("\n", end="")
        for y in range(0, len(img_arr[x])):
            char = to_lightness(ascii, img_arr[x][y])
            asc_print(sys.argv[3], char)

elif sys.argv[1] == "lum":
    print("lum")
    for x in range(0, len(img_arr)):
        print("\n", end="")
        for y in range(0, len(img_arr[x])):
            char = to_luminosity(ascii, img_arr[x][y])
            asc_print(sys.argv[3], char)

deinit()
