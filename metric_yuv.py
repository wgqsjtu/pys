import os
import subprocess
import time
import numpy as np
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from bjontegaard_metric import BD_RATE

# ffmpeg -i %d_RBPNF7.png -pix_fmt yuv420p race.yuv

# ffmpeg -s 832x480 -i race.yuv -s 832x480 -i ../../C/RaceHorsesC_832x480_30.yuv -vframes 40 -lavfi psnr="stats_file=race_psnr.log" -f null -

#yuv_path = '/home/wgq/research/hw/vsr/bicubic_test/LP/'

def seq_qp(log):
    if 'Basket' in log:
        return [18, 24, 30, 36, 51]
    if 'BQT' in log:
        return [15, 24, 30, 36, 42]
    if 'Cactus' in log:
        return [18, 25, 30, 37, 42]
    if 'MarketP' in log:
        return [20, 25, 30, 37, 42]
    if 'Ritual' in log:
        return [20, 25, 30, 36, 42]

def select_qp(seq, qp = [0, 0, 0, 0, 0]):
    if qp == [0, 0, 0, 0, 0]:
        qp = seq_qp(seq)
    for i in qp:
        if str(i) in seq:
            return True
    return False



# 计算bdbr RD曲线
def cal_bdbr_rd(ref, test, seq, qp, net1, net2, conf):

    test = test[test['seq'] == seq]
    test = test[(test.qp == qp[0])|(test.qp == qp[1])|(test.qp == qp[2])|(test.qp == qp[3])]
    ref = ref[ref['seq'] == seq]
    #计算BDBR
    psnr_bdrate = BD_RATE(np.array(ref.loc[:, 'bitrate'], dtype=float), np.array(ref.loc[:, 'psnr_y'], dtype=float), np.array(test.loc[:, 'bitrate'], dtype=float), np.array(test.loc[:, 'psnr_y'], dtype=float))
    ssim_bdrate = BD_RATE(np.array(ref.loc[:, 'bitrate'], dtype=float), np.array(ref.loc[:, 'ssim_y'], dtype=float), np.array(test.loc[:, 'bitrate'], dtype=float), np.array(test.loc[:, 'ssim_y'], dtype=float))
    msssim_bdrate = BD_RATE(np.array(ref.loc[:, 'bitrate'], dtype=float), np.array(ref.loc[:, 'ms-ssim'], dtype=float), np.array(test.loc[:, 'bitrate'], dtype=float), np.array(test.loc[:, 'ms-ssim'], dtype=float))
    vmaf_bdrate = BD_RATE(np.array(ref.loc[:, 'bitrate'], dtype=float), np.array(ref.loc[:, 'vmaf'], dtype=float), np.array(test.loc[:, 'bitrate'], dtype=float), np.array(test.loc[:, 'vmaf'], dtype=float))
    print(seq, psnr_bdrate, ssim_bdrate, msssim_bdrate, vmaf_bdrate)
    # RD曲线 PSNR
    fig, ax = plt.subplots()
    ax.plot(ref.loc[:, 'bitrate'], ref.loc[:, 'psnr_y'], label = net1, marker='^', markersize=8, linewidth=2.0)
    ax.plot(test.loc[:, 'bitrate'], test.loc[:, 'psnr_y'], label = net2, marker='^', markersize=8, linewidth=2.0)
    ax.legend(fontsize=15)
    plt.xlabel('Bitrate',fontsize=15)
    plt.ylabel('PSNR',fontsize=15)
    plt.savefig(fname = seq + '_' + net1 + '_' + net2 + '_' + conf + '_' + 'pnsr.png', dpi=500)
     # RD曲线 SSIM
    fig, ax = plt.subplots()
    ax.plot(ref.loc[:, 'bitrate'], ref.loc[:, 'ssim_y'], label = net1, marker='^', markersize=8, linewidth=2.0)
    ax.plot(test.loc[:, 'bitrate'], test.loc[:, 'ssim_y'], label = net2, marker='^', markersize=8, linewidth=2.0)
    ax.legend(fontsize=15)
    plt.xlabel('Bitrate',fontsize=15)
    plt.ylabel('SSIM',fontsize=15)
    plt.savefig(fname = seq + '_' + net1 + '_' + net2 + '_' + conf + '_' + 'ssim.png', dpi=500)

     # RD曲线 SSIM
    fig, ax = plt.subplots()
    ax.plot(ref.loc[:, 'bitrate'], ref.loc[:, 'ms-ssim'], label = net1, marker='^', markersize=8, linewidth=2.0)
    ax.plot(test.loc[:, 'bitrate'], test.loc[:, 'ms-ssim'], label = net2, marker='^', markersize=8, linewidth=2.0)
    ax.legend(fontsize=15)
    plt.xlabel('Bitrate',fontsize=15)
    plt.ylabel('MS-SSIM',fontsize=15)
    plt.savefig(fname = seq + '_' + net1 + '_' + net2 + '_' + conf + '_' + 'ms-ssim.png', dpi=500)

     # RD曲线 SSIM
    fig, ax = plt.subplots()
    ax.plot(ref.loc[:, 'bitrate'], ref.loc[:, 'vmaf'], label = net1, marker='^', markersize=8, linewidth=2.0)
    ax.plot(test.loc[:, 'bitrate'], test.loc[:, 'vmaf'], label = net2, marker='^', markersize=8, linewidth=2.0)
    ax.legend(fontsize=15)
    plt.xlabel('Bitrate',fontsize=15)
    plt.ylabel('VMAF',fontsize=15)
    plt.savefig(fname = seq + '_' + net1 + '_' + net2 + '_' + conf + '_' + 'vmaf.png', dpi=500)

    plt.cla()
    plt.close("all")

#yuv_path = '/home/wgq/research/hw/vsr/bicubic_test/LP/'
#yuv_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'
yuv_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_yuv/LP/'
seq_path = '/home/wgq/research/VVCSeq/B/'
# 计算psnr
if 0:
    # yuv_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'
    #yuv_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_yuv/LP/'


    yuv_name = [f for f in os.listdir(yuv_path)]
    yuv_name.sort()
    for yuv in yuv_name:
        if yuv.endswith('yuv'):
            if 'Basket' in yuv or 'Cactus' in yuv:
                frames = 49
            else:
                frames = 65
            name = yuv.split('_')[2]
            seq_name = [f for f in os.listdir(seq_path)]
            for seq in seq_name:
                if name in seq:   #-f null -
                    cmd = 'ffmpeg -s 1920x1080 -i ' + yuv_path + yuv + ' -s 1920x1080 -i ' + seq_path + seq + ' -vframes ' + str(frames) + ' -lavfi psnr -f null - 2> ' + yuv_path + yuv.split('.')[0] + '_psnr.log' #-vframes 40
                    print(cmd)
                    subprocess.Popen(cmd, shell=True)
                    time.sleep(0.01)
                    cmd = 'ffmpeg -s 1920x1080 -i ' + yuv_path + yuv + ' -s 1920x1080 -i ' + seq_path + seq + ' -vframes ' + str(frames) + ' -lavfi ssim -f null - 2> ' + yuv_path + yuv.split('.')[0] + '_ssim.log'
                    print(cmd)
                    subprocess.Popen(cmd, shell=True)
                    time.sleep(0.01)
                    cmd = './vmaf/vmaf --reference ' + seq_path + seq + ' --distorted ' +  yuv_path + yuv + ' --width 1920 --height 1080 --pixel_format 420 --bitdepth 8 --model version=vmaf_v0.6.1 --feature float_ms_ssim --output ' + yuv_path + yuv.split('.')[0] + '_vmaf.log'
                    print(cmd)
                    subprocess.Popen(cmd, shell=True)
                    time.sleep(0.01)
# 统计psnr
if 0:

    flog = open(yuv_path + 'metric.log', 'w')
    log_path = [f for f in os.listdir(yuv_path)]
    log_path.sort()
    for log in log_path:
        if log.endswith('psnr.log'):
            name = log.split('_')[2]
            qp = log.split('_')[3]
            metric = 'psnr'
            file = open(yuv_path + log, 'r')
            line = file.readline()
            while not line.startswith('[Parsed_psnr_'):
                line = file.readline()
            flog.write(name+'_' + qp + '_' + metric + ': ' + line.split('] ')[1])
            os.remove(yuv_path + log)

        if log.endswith('ssim.log'):
            name = log.split('_')[2]
            qp = log.split('_')[3]
            metric = 'ssim'
            file = open(yuv_path + log, 'r')
            line = file.readline()
            while not line.startswith('[Parsed_ssim_'):
                line = file.readline()
            flog.write(name+'_' + qp + '_' + metric + ': ' + line.split('] ')[1])
            os.remove(yuv_path + log)

        if log.endswith('vmaf.log'):
            name = log.split('_')[2]
            qp = log.split('_')[3]
            file = open(yuv_path + log, 'r')
            line = file.readline()
            while not line.startswith('    <metric name="float_ms_ssim'):
                line = file.readline()
            flog.write(name+'_' + qp + '_' + 'ms-ssim' + ': ' + line.split('\"')[7] + '\n')
            line = file.readline()
            flog.write(name+'_' + qp + '_' + 'vmaf' + ': ' + line.split('\"')[7] + '\n')
            os.remove(yuv_path + log)
    flog.write('###')
    flog.close()

# RD曲线 bicbic vs HPM (RA)
if 0:

    ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/bicubic_test/FullR/'
    test_metric_log = open(metric_path + 'metric.log', 'r')
    df = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = test_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df.loc[i, 'seq'] = line.split('_')[0]
            df.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])
            i = i + 1
    # print(df)

    test_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/HalfResolution/log/'
    str_log_path = [f for f in os.listdir(test_str_log_path)]

    #allqp = [22, 27, 32, 37, 42, 47, 52, 57, 62]
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_RA' in log) and select_qp(log):
                seq = log.split('_')[2]
                qp = int(log.split('_')[3].split('qp')[1])
                log_file = open(test_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df[df.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    #print(df)

    ## 直接编
    ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'
    ref_metric_log = open(metric_path + 'metric.log', 'r')
    df_ref = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = ref_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df_ref.loc[i, 'seq'] = line.split('_')[0]
            df_ref.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df_ref.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df_ref.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])
            i = i + 1
    # print(df)

    ref_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/log/'
    str_log_path = [f for f in os.listdir(ref_str_log_path)]

    allqp = [27, 32, 38, 45, 51]
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_RA' in log) and select_qp(log):
                seq = log.split('_')[2]
                qp = int(log.split('_')[3].split('qp')[1])
                log_file = open(test_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df_ref[df_ref.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df_ref.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    print(df_ref)
    # plot RD, 计算BDBR


    # BasketballDrive 18, 24, 30, 36, 51
    # BQTerrace 15, 24, 30, 36, 42
    # Cactus 18, 25, 30, 37, 42
    # MarketPlace 20, 25, 30, 37, 42
    # RitualDance # 20, 25, 30, 36, 42

    HalfR_qp = [32, 38, 45, 51]
    df_low = df_ref[(df_ref.qp == HalfR_qp[0])|(df_ref.qp == HalfR_qp[1])|(df_ref.qp == HalfR_qp[2])|(df_ref.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_low, df, 'BasketballDrive', [24, 30, 36, 51], 'Anchor', 'Bicubic', 'RA_lowbitrate')
    cal_bdbr_rd(df_low, df, 'BQTerrace', [24, 30, 36, 42], 'Anchor', 'Bicubic', 'RA_lowbitrate')
    cal_bdbr_rd(df_low, df, 'Cactus', [25, 30, 37, 42], 'Anchor', 'Bicubic', 'RA_lowbitrate')
    cal_bdbr_rd(df_low, df, 'MarketPlace', [25, 30, 37, 42], 'Anchor', 'Bicubic', 'RA_lowbitrate')
    cal_bdbr_rd(df_low, df, 'RitualDance', [25, 30, 36, 42], 'Anchor', 'Bicubic', 'RA_lowbitrate')

    HalfR_qp = [27, 32, 38, 45]
    df_high = df_high[(df_high.qp == HalfR_qp[0])|(df_high.qp == HalfR_qp[1])|(df_high.qp == HalfR_qp[2])|(df_high.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_high, df, 'BasketballDrive', [18, 24, 30, 36], 'Anchor', 'Bicubic', 'RA_highbitrate')
    cal_bdbr_rd(df_high, df, 'BQTerrace', [15, 24, 30, 36], 'Anchor', 'Bicubic', 'RA_highbitrate')
    cal_bdbr_rd(df_high, df, 'Cactus', [18, 25, 30, 37], 'Anchor', 'Bicubic', 'RA_highbitrate')
    cal_bdbr_rd(df_high, df, 'MarketPlace', [20, 25, 30, 37], 'Anchor', 'Bicubic', 'RA_highbitrate')
    cal_bdbr_rd(df_high, df, 'RitualDance', [20, 25, 30, 36], 'Anchor', 'Bicubic', 'RA_highbitrate')

# RD曲线 bicbic vs HPM (LP)
if 0:

   ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/bicubic_test/LP/'
    test_metric_log = open(metric_path + 'metric.log', 'r')
    df = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'ms-ssim', 'vmaf', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = test_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df.loc[i, 'seq'] = line.split('_')[0]
            df.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])

        if metric == 'ms-ssim':
            df.loc[i, 'ms-ssim'] = float(line.split(':')[1])
        if metric == 'vmaf':
            df.loc[i, 'vmaf'] = float(line.split(':')[1])
            i = i + 1

    # print(df)

    test_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/HalfResolution/log/'
    str_log_path = [f for f in os.listdir(test_str_log_path)]
    str_log_path.sort()
    i = 0
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_LP' in log) and select_qp(log):
                seq = log.split('_')[2]
                qp = int(log.split('.')[0].split('_')[3].split('qp')[1])
                log_file = open(test_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df[df.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    print(df)

    ## 直接编
    ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'
    ref_metric_log = open(metric_path + 'metric.log', 'r')
    df_ref = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'ms-ssim', 'vmaf', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = ref_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df_ref.loc[i, 'seq'] = line.split('_')[0]
            df_ref.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df_ref.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df_ref.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])

        if metric == 'ms-ssim':
            df_ref.loc[i, 'ms-ssim'] = float(line.split(':')[1])
        if metric == 'vmaf':
            df_ref.loc[i, 'vmaf'] = float(line.split(':')[1])
            i = i + 1
    # print(df)

    ref_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/log/'
    str_log_path = [f for f in os.listdir(ref_str_log_path)]

    allqp = [27, 32, 38, 45, 51]
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_LP' in log) and select_qp(log, allqp):
                seq = log.split('_')[2]
                qp = int(log.split('.')[0].split('_')[3].split('qp')[1])
                log_file = open(ref_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df_ref[df_ref.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df_ref.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    print(df_ref)
    # plot RD, 计算BDBR


    # BasketballDrive 18, 24, 30, 36, 51
    # BQTerrace 15, 24, 30, 36, 42
    # Cactus 18, 25, 30, 37, 42
    # MarketPlace 20, 25, 30, 37, 42
    # RitualDance # 20, 25, 30, 36, 42

    HalfR_qp = [32, 38, 45, 51]
    df_low = df_ref[(df_ref.qp == HalfR_qp[0])|(df_ref.qp == HalfR_qp[1])|(df_ref.qp == HalfR_qp[2])|(df_ref.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_low, df, 'BasketballDrive', [24, 30, 36, 51], 'Anchor', 'Bicubic', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'BQTerrace', [24, 30, 36, 42], 'Anchor', 'Bicubic', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'Cactus', [25, 30, 37, 42], 'Anchor', 'Bicubic', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'MarketPlace', [25, 30, 37, 42], 'Anchor', 'Bicubic', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'RitualDance', [25, 30, 36, 42], 'Anchor', 'Bicubic', 'LP_lowbitrate')

    HalfR_qp = [27, 32, 38, 45]
    df_high = df_ref[(df_ref.qp == HalfR_qp[0])|(df_ref.qp == HalfR_qp[1])|(df_ref.qp == HalfR_qp[2])|(df_ref.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_high, df, 'BasketballDrive', [18, 24, 30, 36], 'Anchor', 'Bicubic', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'BQTerrace', [15, 24, 30, 36], 'Anchor', 'Bicubic', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'Cactus', [18, 25, 30, 37], 'Anchor', 'Bicubic', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'MarketPlace', [20, 25, 30, 37], 'Anchor', 'Bicubic', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'RitualDance', [20, 25, 30, 36], 'Anchor', 'Bicubic', 'LP_highbitrate')

# RD曲线 RBPN vs HPM (RA)
if 0:

    # RBPN
    metric_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_yuv/RA/'
    test_metric_log = open(yuv_path + 'metric.log', 'r')
    df = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = test_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df.loc[i, 'seq'] = line.split('_')[0]
            df.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])
            i = i + 1
    # print(df)

    test_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/HalfResolution/log/'
    str_log_path = [f for f in os.listdir(test_str_log_path)]

    allqp = [22, 27, 32, 37, 42, 47, 52, 57, 62]
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_RA' in log) and select_qp(log):
                seq = log.split('_')[2]
                qp = int(log.split('_')[3].split('qp')[1])
                log_file = open(test_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df[df.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    #print(df)

    ## 直接编
    ref_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/log/'
    str_log_path = [f for f in os.listdir(ref_str_log_path)]
    str_log_path.sort()

    df_ref = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'bitrate'])
    #allqp = [22, 27, 32, 37, 42, 47, 52, 57, 62]
    i = 0
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_RA' in log):
                seq = log.split('_')[2]
                qp = int(log.split('_')[3].split('qp')[1])
                log_file = open(ref_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  PSNR Y(dB)'):
                    line = log_file.readline()
                df_ref.loc[i, 'seq'] = seq
                df_ref.loc[i, 'qp'] = qp
                # print(line.split('_')[1].split('qp')[1])
                df_ref.loc[i, 'psnr_y'] = float(line.split(':')[1])
                df_ref.loc[i, 'psnr_u'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'psnr_v'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_y'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_u'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_v'] = float(log_file.readline().split(':')[1])
                log_file.readline()
                #print(i)
                #print(float(line.split(':')[1]))
                df_ref.loc[i, 'bitrate'] = float(log_file.readline().split(':')[1])
                log_file.close()
                i = i + 1
    #df_ref = df_ref.sort_index()
    #print(df_ref)

    # plot RD, 计算BDBR
    HalfR_qp = [32, 37, 42, 47]
    df_low = df[(df.qp == HalfR_qp[0])|(df.qp == HalfR_qp[1])|(df.qp == HalfR_qp[2])|(df.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_ref, df_low, 'BasketballDrive', [41, 46, 51, 62], 'Anchor', 'RBPN', 'RA_lowbitrate')
    cal_bdbr_rd(df_ref, df_low, 'BQTerrace', [42, 47, 52, 56], 'Anchor', 'RBPN', 'RA_lowbitrate')
    cal_bdbr_rd(df_ref, df_low, 'Cactus', [41, 45, 51, 57], 'Anchor', 'RBPN', 'RA_lowbitrate')
    cal_bdbr_rd(df_ref, df_low, 'MarketPlace', [40, 45, 50, 57], 'Anchor', 'RBPN', 'RA_lowbitrate')
    cal_bdbr_rd(df_ref, df_low, 'RitualDance', [40, 45, 50, 63], 'Anchor', 'RBPN', 'RA_lowbitrate')

    HalfR_qp = [27, 32, 37, 42]
    df_high = df[(df.qp == HalfR_qp[0])|(df.qp == HalfR_qp[1])|(df.qp == HalfR_qp[2])|(df.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_ref, df_high, 'BasketballDrive', [36, 41, 46, 51], 'Anchor', 'RBPN', 'RA_highbitrate')
    cal_bdbr_rd(df_ref, df_high, 'BQTerrace', [37, 42, 47, 52], 'Anchor', 'RBPN', 'RA_highbitrate')
    cal_bdbr_rd(df_ref, df_high, 'Cactus', [37, 41, 45, 51], 'Anchor', 'RBPN', 'RA_highbitrate')
    cal_bdbr_rd(df_ref, df_high, 'MarketPlace', [35, 40, 45, 50], 'Anchor', 'RBPN', 'RA_highbitrate')
    cal_bdbr_rd(df_ref, df_high, 'RitualDance', [34, 40, 45, 50], 'Anchor', 'RBPN', 'RA_highbitrate')

# RD曲线 RBPN vs HPM (LP)
if 1:

    ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/RBPN_test/RBPN_FullR_yuv/LP/'
    test_metric_log = open(metric_path + 'metric.log', 'r')
    df = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'ms-ssim', 'vmaf', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = test_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df.loc[i, 'seq'] = line.split('_')[0]
            df.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])

        if metric == 'ms-ssim':
            df.loc[i, 'ms-ssim'] = float(line.split(':')[1])
        if metric == 'vmaf':
            df.loc[i, 'vmaf'] = float(line.split(':')[1])
            i = i + 1

    # print(df)

    test_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/HalfResolution/log/'
    str_log_path = [f for f in os.listdir(test_str_log_path)]
    str_log_path.sort()
    i = 0
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_LP' in log) and select_qp(log):
                seq = log.split('_')[2]
                qp = int(log.split('.')[0].split('_')[3].split('qp')[1])
                log_file = open(test_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df[df.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    print(df)

    ## 直接编
    ## bicubic
    metric_path = '/home/wgq/research/hw/vsr/AVS_dec/FullResolution/'
    ref_metric_log = open(metric_path + 'metric.log', 'r')
    df_ref = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'ms-ssim', 'vmaf', 'bitrate'])
    line = ''
    i = 0
    while 1:
        line = ref_metric_log.readline()
        if '##' in line:
            break
        metric = line.split('_')[2].split(':')[0]
        if metric == 'psnr':

            df_ref.loc[i, 'seq'] = line.split('_')[0]
            df_ref.loc[i, 'qp'] = int(line.split('_')[1].split('qp')[1])
            # print(line.split('_')[1].split('qp')[1])
            df_ref.loc[i, 'psnr_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'psnr_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'psnr_v'] = float(line.split(':')[4].split(' ')[0])
        if metric == 'ssim':
            df_ref.loc[i, 'ssim_y'] = float(line.split(':')[2].split(' ')[0])
            df_ref.loc[i, 'ssim_u'] = float(line.split(':')[3].split(' ')[0])
            df_ref.loc[i, 'ssim_v'] = float(line.split(':')[4].split(' ')[0])

        if metric == 'ms-ssim':
            df_ref.loc[i, 'ms-ssim'] = float(line.split(':')[1])
        if metric == 'vmaf':
            df_ref.loc[i, 'vmaf'] = float(line.split(':')[1])
            i = i + 1
    # print(df)

    ref_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/log/'
    str_log_path = [f for f in os.listdir(ref_str_log_path)]

    allqp = [27, 32, 38, 45, 51]
    for log in str_log_path:
        if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
            if ('enc_LP' in log) and select_qp(log, allqp):
                seq = log.split('_')[2]
                qp = int(log.split('.')[0].split('_')[3].split('qp')[1])
                log_file = open(ref_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  bitrate(kbps)'):
                    line = log_file.readline()
                df_t = df_ref[df_ref.seq == seq]
                df_t = df_t[df_t.qp == qp]
                index = df_t.index.tolist()[0]
                #print(index)
                #print(float(line.split(':')[1]))
                df_ref.loc[index, 'bitrate'] = float(line.split(':')[1])
                log_file.close()
    print(df_ref)
    # plot RD, 计算BDBR


    # BasketballDrive 18, 24, 30, 36, 51
    # BQTerrace 15, 24, 30, 36, 42
    # Cactus 18, 25, 30, 37, 42
    # MarketPlace 20, 25, 30, 37, 42
    # RitualDance # 20, 25, 30, 36, 42

    HalfR_qp = [32, 38, 45, 51]
    df_low = df_ref[(df_ref.qp == HalfR_qp[0])|(df_ref.qp == HalfR_qp[1])|(df_ref.qp == HalfR_qp[2])|(df_ref.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_low, df, 'BasketballDrive', [24, 30, 36, 51], 'Anchor', 'RBPN', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'BQTerrace', [24, 30, 36, 42], 'Anchor', 'RBPN', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'Cactus', [25, 30, 37, 42], 'Anchor', 'RBPN', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'MarketPlace', [25, 30, 37, 42], 'Anchor', 'RBPN', 'LP_lowbitrate')
    cal_bdbr_rd(df_low, df, 'RitualDance', [25, 30, 36, 42], 'Anchor', 'RBPN', 'LP_lowbitrate')

    HalfR_qp = [27, 32, 38, 45]
    df_high = df_ref[(df_ref.qp == HalfR_qp[0])|(df_ref.qp == HalfR_qp[1])|(df_ref.qp == HalfR_qp[2])|(df_ref.qp == HalfR_qp[3])]
    cal_bdbr_rd(df_high, df, 'BasketballDrive', [18, 24, 30, 36], 'Anchor', 'RBPN', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'BQTerrace', [15, 24, 30, 36], 'Anchor', 'RBPN', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'Cactus', [18, 25, 30, 37], 'Anchor', 'RBPN', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'MarketPlace', [20, 25, 30, 37], 'Anchor', 'RBPN', 'LP_highbitrate')
    cal_bdbr_rd(df_high, df, 'RitualDance', [20, 25, 30, 36], 'Anchor', 'RBPN', 'LP_highbitrate')

# HPM码率统计
if 0:
    ref_str_log_path = '/home/wgq/research/hw/vsr/AVS_str/FullResolution/log/'
    str_log_path = [f for f in os.listdir(ref_str_log_path)]
    str_log_path.sort()

    df_ref = pd.DataFrame(columns=['seq', 'qp', 'psnr_y', 'psnr_u', 'psnr_v', 'ssim_y', 'ssim_u', 'ssim_v', 'bitrate'])
    # allqp = [22, 27, 32, 37, 42, 47, 52, 57, 62]
    i = 0
    for log in str_log_path:
        #if 'Basket' in log or 'BQT' in log or 'Cactus' in log or 'MarketP' in log or 'Ritual' in log:
        # if 'BQT' in log or 'MarketP' in log or 'Ritual' in log:
        if 1:
            if ('enc' in log):
                seq = log.split('_')[2]
                if 'RA' in log:
                    qp = int(log.split('_')[3].split('qp')[1])
                    seq = 'RA_' + seq
                if 'LP' in log:
                    qp = int(log.split('.')[0].split('_')[3].split('qp')[1])
                    seq = 'LP_' + seq
                log_file = open(ref_str_log_path + log, 'r')
                line = log_file.readline()
                while not line.startswith('  PSNR Y(dB)'):
                    line = log_file.readline()
                df_ref.loc[i, 'seq'] = seq
                df_ref.loc[i, 'qp'] = qp
                # print(line.split('_')[1].split('qp')[1])
                df_ref.loc[i, 'psnr_y'] = float(line.split(':')[1])
                df_ref.loc[i, 'psnr_u'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'psnr_v'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_y'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_u'] = float(log_file.readline().split(':')[1])
                df_ref.loc[i, 'ssim_v'] = float(log_file.readline().split(':')[1])
                log_file.readline()
                df_ref.loc[i, 'bitrate'] = float(log_file.readline().split(':')[1])
                log_file.close()
                i = i + 1
    df_ref = df_ref.sort_index()
    df_ref.to_csv('HPM_FullR_RD.csv')

















