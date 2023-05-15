import os
import subprocess
import scipy
import re
import numpy as np
import matplotlib.pyplot as plt
from yuv420 import readYUV420, readYUV420Range, writeYUV420


def calculate_psnr(compressed_path, original_path='./data/dancing_org.1280x548.yuv'):
    cmd = f'ffmpeg -s:v 1280x548 -i {original_path} -s:v 1280x548 -i {compressed_path} -lavfi psnr -f null -'
    psnr_output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode()
    psnr_line = psnr_output.split('\n')[-2]
    match = re.search(r"average:([\d.]+)", psnr_line)
    psnr = 0
    if match:
        psnr = float(match.group(1))
    return psnr


def convert_yuv_to_mp4(input_dir, output_dir):
    # Convert YUV files to yuv format for different bitrates and resolutions
    for i in range(len(resolutions)):
        yuv_file = os.path.join(input_dir, f"dancing.{resolutions[i][0]}x{resolutions[i][1]}.yuv")
        for j in range(len(bitrates[i])):
            bitrate = bitrates[i][j]
            output_file = os.path.join(output_dir, f"dancing_{resolutions[i][0]}x{resolutions[i][1]}_{bitrate}k.yuv")
            cmd = f"ffmpeg -s {resolutions[i][0]}x{resolutions[i][1]} -pix_fmt yuv420p -i {yuv_file} -b:v {bitrate}k -vcodec libx264 -pix_fmt yuv420p {output_file}"
            os.system(cmd)


def convert_mp4_to_yuv(input_dir, output_dir):
    # Convert mp4 files to yuv format for different bitrates and resolutions
    for i in range(len(resolutions)):
        for j in range(len(bitrates[i])):
            bitrate = bitrates[i][j]
            mp4_file = os.path.join(input_dir, f"dancing_{resolutions[i][0]}x{resolutions[i][1]}_{bitrate}k.mp4")
            output_file = os.path.join(output_dir, f"dancing_{resolutions[i][0]}x{resolutions[i][1]}_{bitrate}k.yuv")
            cmd = f'ffmpeg -i {mp4_file} -pix_fmt yuv420p -f rawvideo {output_file}'
            os.system(cmd)


def upsample_resolutions(input_dir, output_dir):
    for i in range(len(resolutions)):
        if i == 0:
            continue

        for j in range(len(bitrates[i])):
            bitrate = bitrates[i][j]
            yuv_file = os.path.join(input_dir, f"dancing_{resolutions[i][0]}x{resolutions[i][1]}_{bitrate}k.yuv")
            output_file = os.path.join(output_dir, f"dancing_1280x720_from_{resolutions[i][0]}x{resolutions[i][1]}_{bitrate}k.yuv")
            cmd = f'ffmpeg -s {resolutions[i][0]}x{resolutions[i][1]} -pix_fmt yuv420p -i {yuv_file} -vf "scale=1280:548:flags=bicubic" -pix_fmt yuv420p {output_file}'
            os.system(cmd)


def get_all_psnr():
    psnr_list = []
    psnr_list.append(calculate_psnr('./upsample/dancing_1280x720_from_640x274_96k.yuv'))
    psnr_list.append(calculate_psnr('./upsample/dancing_1280x720_from_640x274_128k.yuv'))
    psnr_list.append(calculate_psnr('./upsample/dancing_1280x720_from_640x274_256k.yuv'))
    return psnr_list


if __name__ == '__main__':
    input_dir = "./data/"
    output_dir = "./output/"

    resolutions = [(1280, 548), (640, 274), (320, 138)]
    bitrates = [
        [512, 1024, 2048, 3072],
        [96, 128, 256, 384, 512, 1024, 2048],
        [64, 96, 128, 256, 512, 1024]
    ]

    # convert_yuv_to_mp4("./data/", "./output/")
    # convert_mp4_to_yuv("./output/", "yuv/")
    # upsample_resolutions("./yuv/", "./upsample/")


    print(get_all_psnr())

    # ffmpeg -s 320x138 -pix_fmt yuv180p -i dancing_320x138_64k.yuv -vf "scale=1280:548:flags=bicubic" -pix_fmt test output.yuv
    # ffmpeg -s 320x138 -pix_fmt yuv420p -i dancing_320x138_64k.yuv -vf "scale=1280:548:flags=bicubic" -pix_fmt yuv420p output.yuv
    # dancing_320x138_64k.yuv