import os
import subprocess
import time
import numpy as np
import shutil

# ffmpeg -i %d_RBPNF7.png -pix_fmt yuv420p race.yuv

# ffmpeg -s 832x480 -i race.yuv -s 832x480 -i ../../C/RaceHorsesC_832x480_30.yuv -vframes 40 -lavfi psnr="stats_file=race_psnr.log" -f null -

image_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_png/LP/'
yuv_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_yuv/LP/'
seq_path = '/home/wgq/research/VVCSeq/B/'

image_name = [f for f in os.listdir(image_path)]
for i_name in image_name:
    name = i_name.split('_')[0]
    cmd = 'ffmpeg -i ' + image_path + i_name + '/%d_RBPNF7.png -pix_fmt yuv420p ' + yuv_path + i_name + '.yuv'
    print(cmd)
    subprocess.Popen(cmd, shell=True)
    time.sleep(0.01)
    # seq_name = [f for f in os.listdir(seq_path)]
    # for seq in seq_name:
    #     if name in seq:   #-f null -
    #         cmd = 'ffmpeg -s 832x480 -i ' + yuv_path + i_name + '.yuv' + ' -s 832x480 -i ' + seq_path + seq + ' -vframes 40 -lavfi psnr -f null - 2> ' + yuv_path + i_name + '_psnr.log'
    #         #print(cmd)
    #         os.system(cmd)
    #         cmd = 'ffmpeg -s 832x480 -i ' + yuv_path + i_name + '.yuv' + ' -s 832x480 -i ' + seq_path + seq + ' -vframes 40 -lavfi ssim -f null - 2> ' + yuv_path + i_name + '_ssim.log'
            #print(cmd)
            #os.system(cmd)

# flog = open(yuv_path + 'metric.log', 'w')
# log_path = [f for f in os.listdir(yuv_path)]
# for log in log_path:
#     if log.endswith('psnr.log'):
#         file = open(yuv_path + log, 'r')
#         line = file.readline()
#         while not line.startswith('[Parsed_psnr_'):
#             line = file.readline()
#         flog.write(log + ': ' + line + '\n')
#     if log.endswith('ssim.log'):
#         file = open(yuv_path + log, 'r')
#         line = file.readline()
#         while not line.startswith('[Parsed_ssim_'):
#             line = file.readline()
#         flog.write(log + ': ' + line + '\n')
# flog.close()




