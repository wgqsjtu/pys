import os
import subprocess
import time

#ffmpeg -s 3840x2160 -pix_fmt yuv420p –i A1/FoodMarket4_3840x2160_60fps_8bit_420.yuv -vframes 40 Food/%03d.png

in_path = '/home/wgq/research/hw/vsr/AVS_dec/HalfResolution/'
out_path = '/home/wgq/research/hw/vsr/RBPN_test/HalfR/'

if os.path.exists(out_path) == 0:
    os.mkdir(out_path)

def select_size(seq):
    if 'Basket' in seq or 'BQT' in seq or 'Cactus' in seq or 'MarketP' in seq or 'Ritual' in seq:
        return '960*540'
    if 'Cam' in seq or 'CatR' in seq or 'Day' in seq or 'Food' in seq or 'Park' in seq or 'Tango' in seq:
        return '1920*1080'

# size = '416*240'
image_path = [f for f in os.listdir(in_path)]

for image in image_path:
    if image.endswith('yuv'):
        name = image.split('.yuv')[0]
        size = select_size(image)
        if size == '960*540' and ('LP' in image):
            if os.path.exists(out_path + name) == 0:
                os.mkdir(out_path + name)
            size = select_size(image)
            cmd = 'ffmpeg ' + '-s ' + size  + ' -pix_fmt yuv420p10le' + ' -i ' + in_path + image + ' ' + out_path + name + '/%03d.png' # -vframes 20
            #print(cmd)
            subprocess.Popen(cmd, shell=True)
            time.sleep(0.01)