import json
import subprocess
import re
import matplotlib.pyplot as plt


def traverse_qp(qp):
    # Excuting an order
    cmd = f'ffmpeg -i .\dancing.mp4 -vcodec libx264 -qp {qp} -psnr ./qp/out_{qp}_qp.mp4'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # extract numbers
    output = result.stdout.decode('utf-8')
    # print(output)
    psnr_match = re.search(r'] PSNR Mean Y:([\d.]+)', output)
    psnr = float(psnr_match.group(1))
    kbps_match = re.search(r'kb/s:([\d.]+)', output)
    kbps = float(kbps_match.group(1))

    # print result
    print(f'qp: {qp}, PSNR: {psnr}, kbps: {kbps}')
    return psnr, kbps


def traverse_rate(rate):
    # Excuting an order
    cmd = f'ffmpeg -i .\dancing.mp4 -b:v {rate}k -vcodec: libx264 -psnr ./rate/out_{rate}k.mp4'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # extract numbers
    output = result.stdout.decode('utf-8')
    # print(output)
    psnr_match = re.search(r'] PSNR Mean Y:([\d.]+)', output)
    psnr = float(psnr_match.group(1))
    kbps_match = re.search(r'kb/s:([\d.]+)', output)
    kbps = float(kbps_match.group(1))

    # print result
    print(f'rate: {rate}, PSNR: {psnr}, kbps: {kbps}')
    return psnr, kbps


def get_frame_rate(info):
    # get framerate from video stream
    for stream in info['streams']:
        if stream['codec_type'] == 'video':
            framerate = stream['r_frame_rate']
            break

    # print framerate
    print(f'Video framerate: {framerate} fps')


def get_duration(info):
    # get duration from format section
    duration = int(float(info['format']['duration']) + 0.5)  # round off to the nearest second

    # print duration
    print(f'Video duration: {duration} secs')


def get_bit_rate(info):
    # get video bitrate from video stream
    for stream in info['streams']:
        if stream['codec_type'] == 'video':
            bitrate = int(stream['bit_rate']) // 1000  # convert to kbps
            break

    # print video bitrate
    print(f'Video bitrate: {bitrate} kbps')


def get_codec(info):
    # get video codec from video stream
    for stream in info['streams']:
        if stream['codec_type'] == 'video':
            codec_name = stream['codec_name']
            break

    # print video codec
    print(f'Video codec: {codec_name}')


def get_elementary_bit_rate(info):
    # get video elementary stream bitrate from format section
    bitrate = int(info['format']['bit_rate']) // 1000  # convert to kbps

    # print video elementary stream bitrate
    print(f'Video elementary stream bitrate: {bitrate} kbps')


def get_info():
    # set the path to the test video
    video_path = 'dancing.mp4'

    # run ffprobe command to get video information
    ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path]
    result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE)

    # parse ffprobe output
    output = result.stdout.decode('utf-8')
    info = json.loads(output)

    # get framerate
    get_frame_rate(info)

    # get duration
    get_duration(info)

    # get video codec
    get_codec(info)

    # get video bitrate
    get_bit_rate(info)

    # get video elementary stream bitrate
    get_elementary_bit_rate(info)


def draw_RD(cbr_psnr_list, cbr_kbps_list, qp_psnr_list, qp_kbps_list):
    # plot the RD curves for constant bitrate and constant QP encoding
    plt.plot(cbr_kbps_list, cbr_psnr_list, 'bo-', label='Constant Bitrate')
    plt.plot(qp_kbps_list, qp_psnr_list, 'r^-', label='Constant QP')

    # set the axis labels and legend
    plt.title('RD Curves for CBR and CQP Encoding')
    plt.xlabel('Bitrate (kbps)')
    plt.ylabel('PSNR (dB)')
    plt.legend()

    # show the plot
    plt.show()


if __name__ == '__main__':
    qp_kbps_list = []
    qp_psnr_list = []
    qp_list = [10, 15, 20, 25, 30, 35, 40, 45]
    for qp in qp_list:
        res = traverse_qp(qp)
        qp_psnr_list.append(res[0])
        qp_kbps_list.append(res[1])

    cbr_kbps_list = []
    cbr_psnr_list = []
    rate_list = [256,512,1024,1536,2048,2560,3072,3584,4096,5120,6144,7168]
    for rate in rate_list:
        res = traverse_rate(rate)
        cbr_psnr_list.append(res[0])
        cbr_kbps_list.append(res[1])

    # get_info()

    draw_RD(cbr_psnr_list, cbr_kbps_list, qp_psnr_list, qp_kbps_list)