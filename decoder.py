from PIL import Image, ImageFile

def find_message_bits(im : ImageFile) -> list[int]:
    w, h = im.size
    hidden_bits = []
    pixels = im.get_flattened_data()
    for pixel in pixels:
        for channel in pixel:
            hidden_bits.append(channel % 2)

    return hidden_bits


def binary_to_decimal(bitList : list[int]) -> int:
    result = 0
    for b in range(len(bitList)):
        result += bitList[b] * (2 ** (len(bitList) - b - 1))

    return result


def binary_to_bytes(data):
    return [data[8 * i:8 * (i + 1)] for i in range(int(len(data) / 8))]


def binary_to_chars(data : list[int]) -> list[chr]:
    byte_list = binary_to_bytes(data)
    char_list = [chr(binary_to_decimal(i)) for i in byte_list]
    return char_list


def parse_text_message(hidden_bits : list[int]) -> str:
    dim_meta_length = 16
    message_length = binary_to_decimal(hidden_bits[:dim_meta_length])
    message_bits = hidden_bits[dim_meta_length:dim_meta_length + message_length]
    message = ''.join(binary_to_chars(message_bits))
    return message


def pixels_from_binary(hidden_bits : list[int]) -> list[int]:
    colour_ints = [i * 255 for i in hidden_bits]
    return colour_ints


def parse_image_data(hidden_bits : list[int]) -> (int, int, list[int]):
    dim_meta_length = 16

    width_end = dim_meta_length
    height_end  = width_end + dim_meta_length

    width = binary_to_decimal(hidden_bits[: width_end])
    height = binary_to_decimal(hidden_bits[width_end : height_end])
    data  = hidden_bits[height_end : height_end + (width * height)]
    return width, height, data

def parse_binary_image(hidden_bits : list[int]) -> Image:
    width, height, image_data = parse_image_data(hidden_bits)

    import numpy as np
    pixels = pixels_from_binary(image_data)
    pix_arr = np.array(pixels).astype(np.uint8).reshape(width, height)

    return Image.fromarray(pix_arr)

def parse_image(filename : str, outfile : str):
    with Image.open(filename) as im:
        hidden_bits = find_message_bits(im)

    header = hidden_bits[:2]
    data = hidden_bits[2:]
    match header[0]:
        case 0:
            with open(f"{outfile}.txt", "w") as output:
                output.write(parse_text_message(data))
        case 1:
            parse_binary_image(data).save(f'{outfile}.bmp')



def main():
    import os

    root = 'images'
    for image in os.listdir(root):
        parse_image(f"{root}/{image}", f"{image}")

main()