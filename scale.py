import os
import subprocess
import time

# ffmpeg -i 001.png  -vf 'scale=0.5*iw:0.5*ih:flags=bicubic' 0001.png
in_path = '/home/wgq/research/hw/vsr/AVS_dec/HalfResolution/'
out_path = '/home/wgq/research/hw/vsr/bicubic_test/LP/'

if os.path.exists(out_path) == 0:
    os.mkdir(out_path)

scale = 2

def select_size(seq):
    if 'Basket' in seq or 'BQT' in seq or 'Cactus' in seq or 'MarketP' in seq or 'Ritual' in seq:
        return '960*540'
    if 'Cam' in seq or 'CatR' in seq or 'Day' in seq or 'Food' in seq or 'Park' in seq or 'Tango' in seq:
        return '1920*1080'

#size = '832*480'
image_path = [f for f in os.listdir(in_path)]

for image in image_path:
    if 'LP' in image:
        size = select_size(image)
        if size == '960*540':
            if image.endswith('yuv'):
                cmd = 'ffmpeg ' + '-s ' + size + ' -pix_fmt yuv420p ' + ' -i ' + in_path + image + ' -vf \'scale=' + str(scale) + '*iw:' + str(scale) + '*ih:flags=bicubic\' ' + out_path + image
            else:
                cmd = 'ffmpeg ' + '-i ' + in_path + image + ' -vf \'scale=' + str(scale) + '*iw:' + str(scale) + '*ih:flags=bicubic\' ' + out_path + image
            print(cmd)
            subprocess.Popen(cmd, shell=True)
            time.sleep(0.01)

