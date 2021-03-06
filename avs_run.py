import os
import subprocess
import time
import numpy as np
import shutil

in_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/'
out_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'

exe_path = '/home/wgq/research/AVS/hw/app_decoder'

if os.path.exists(out_path) == 0:
    os.mkdir(out_path)

seq_path = [f for f in os.listdir(in_path)]

def select_qp(qp, seq):
    for i in qp:
        if str(i) in seq:
            return True
    return False

def dec(s, qp, conf):
    for seq in seq_path:
        if conf in seq and s in seq:
            if select_qp(qp, seq):
                cmd = exe_path + ' -i ' + in_path + seq  + ' -o ' + out_path + seq.split('.')[0] + '.yuv' + ' -d 8'
                print(cmd)
                subprocess.Popen(cmd, shell=True)

# BasketballDrive 18, 24, 30, 36, 51
# BQTerrace 15, 24, 30, 36, 42
# Cactus 18, 25, 30, 37, 42
# MarketPlace 20, 25, 30, 37, 42
# RitualDance # 20, 25, 30, 36, 42
# dec('BasketballDrive', [18, 24, 30, 36, 51], 'LP')
# dec('BQTerrace', [15, 24, 30, 36, 42], 'LP')
# dec('Cactus', [18, 25, 30, 37, 42], 'LP')
# dec('MarketPlace', [20, 25, 30, 37, 42], 'LP')
# dec('RitualDance', [20, 25, 30, 36, 42], 'LP')
dec('BasketballDrive', [27, 32, 38, 45, 51], 'LP')
dec('BQTerrace', [27, 32, 38, 45, 51], 'LP')
dec('Cactus', [27, 32, 38, 45, 51], 'LP')
dec('MarketPlace', [27, 32, 38, 45, 51], 'LP')
dec('RitualDance', [27, 32, 38, 45, 51], 'LP')