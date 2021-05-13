import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import urllib3, hashlib, time, json, base64
import subprocess
import atexit
import ffmpeg
import os
import sys
import scte

#-------------------------------------------------global values

root = r"C:\Users\admin\PycharmProjects\test2"
input_file = r"\2.mp4"
out_file = r"\out.webm"
out = r"\output_gen_file"
video = ffmpeg_streaming.input(root+input_file)

#-------------------------------------------------video manipulation functions
def convert_mp4():
    command = 'ffmpeg -i ' + input_file + ' ' + out_file
    subprocess.run(command)


def video_to_dash():
    dash = video.dash(Formats.h264())
    dash.auto_generate_representations()
    dash.output(r'C:\Users\admin\PycharmProjects\test2\dash.mpd')

    _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    _2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
    _4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

    dash = video.dash(Formats.h264())
    dash.representations(_144p, _240p, _360p, _480p, _720p, _1080p, _2k, _4k)
    dash.output(r'C:\Users\admin\PycharmProjects\test2\dash.mpd')
    atexit.register(print, "Video conversion successfully!")


def video_to_hls():
    _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))

    hls = video.hls(Formats.h264())
    hls.representations(_144p, _240p, _360p, _480p, _720p, _1080p)
    hls.output(root+out+'.m3u8')
    atexit.register(print, "Video conversion successfully!")

def hls_enc():
    #A path you want to save a random key to your local machine
    save_to = '/home/public_html/"PATH TO THE KEY DIRECTORY"/key'

    #A URL (or a path) to access the key on your website
    url = 'http://www.localhost.com/?"PATH TO THE KEY DIRECTORY"/key'
    # or url = '/"PATH TO THE KEY DIRECTORY"/key';

    hls = video.hls(Formats.h264())
    hls.encryption(save_to, url)
    hls.auto_generate_representations()
    hls.output('/var/media/hls.m3u8')


def create_hls_playlist():
    command = '''ffmpeg -y -i 2.mp4 -hls_time 5 -hls_key_info_file enc.keyinfo.txt -hls_playlist_type vod -hls_segment_filename "v%v/segment%d.ts" v%v/index.m3u8'''
    subprocess.run(command)
    atexit.register(print, "Hls playlist creation complete!")

def slicer_integration():
    hs = 'XH7HtD8tR3993IxfbcqX0uhKnc-mYksmPxqM2z1a'
    hs = hs.encode('utf-8')
    secret = '2adf9dd93ca0261ccd04dd879258ef35fa3ff17d'
    timestamp = int(time.time())
    endpoint = '/content_start'
    cnonce = 123
    sig_input = (endpoint + ':' + str(timestamp) + ':' + str(cnonce) + ':' + secret).encode('utf-8')
    sig = base64.b64encode(hashlib.sha1(sig_input).digest())
    body = json.dumps({"timestamp": timestamp,
                       "cnonce": cnonce,
                       "sig": sig})
    request = urllib3.urlopen('http://localhost/hls:65009/' + endpoint, body)
    response = json.loads(request.read())
    assert response['error'] == 0


# --------------------------------------------------input parameters from user #DRIVER CODE#

print('''THIS IS A POC CODE FOR AD-INSERTION
Please enter you preference for video conversion
Select:
1 - for DASH conversion
2 - for HLS conversion
''')

def playlist_driver():
    user_input_sub = input("Do you want to create a playlist for HLS live streaming (y/n): ")
    if user_input_sub == 'y':
        create_hls_playlist()
    if user_input_sub == 'n':
        sys.exit(0)


user_input = int(input("Please enter your preference: "))
if user_input == 1:
    print('You selected video conversion to DASH format. Please wait while the file is being converted...')
    video_to_dash()
    playlist_driver()

if user_input == 2:
    print('You selected video conversion to HLS format. Please wait while the file is being converted...')
    video_to_hls()
    playlist_driver()


# ------------------------------------------------------RESPONSES
# LIST of ads to be inserted
#
# {
# 	"breaks": [{
# 			"age": 19,
# 			"id": 2,
# 			"timecode": "01:01:45;00",
# 			"type": 5,
# 			"type_str": "content start"
# 		}, {
# 			"age": 27,
# 			"id": 1,
# 			"timecode": "01:01:50;00",
# 			"type": 5,
# 			"type_str": "content start"
# 		}
# 	],
# 	"error": 0
# }
#
# AD_POD start response
#
# {
# 	"start_timecode": "00:15:21;09"
# }
#
# AD_POD end response
#
# {
# 	"start_timecode": "00:15:21;09"
# }

