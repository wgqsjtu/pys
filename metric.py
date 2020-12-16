import os
import subprocess
import time
import numpy as np
import shutil

# ffmpeg -i vvc/race/001.png -i Results/vvc/race_4x/1_RBPNF7.png -lavfi psnr="stats_file=psnr.log" -f null -

#ref_path = '/home/wgq/research/hw/RBPN-PyTorch/Vid4/walk/'
#ref_path = '/home/wgq/research/hw/RBPN-PyTorch/Results/vvc/race_2x/'
ref_path = '/home/wgq/research/VVCSeq/scale_2x/C_png/race/'
test_path = '/home/wgq/research/hw/RBPN-PyTorch/Results/vvc/race_2x_2x/'

# file naming rules
ref_name_rule = '.png'
# ref_name_rule = '_RBPNF7.png'
test_name_rule = '_RBPNF7.png'

ref_image_path = [f for f in os.listdir(ref_path)]
test_image_path = [f for f in os.listdir(test_path)]

def check_proc(proc_name):
    Numproc = 0
    file_handle = os.popen('ps -a | grep ' + proc_name + '| wc -l')
    Numproc = int(file_handle.read())
    return Numproc


# cal psnr
for test_image in test_image_path:
    if not test_image.endswith('.log'):
        for ref_image in ref_image_path:
            if int(test_image.split(test_name_rule)[0]) == int(ref_image.split(ref_name_rule)[0]):
                cmd = 'ffmpeg ' + '-i ' + ref_path + ref_image + \
                    ' -i ' + test_path + test_image + \
                    ' -lavfi psnr=\"stats_file=' + test_path + 'psnr' + str(int(test_image.split(test_name_rule)[0])) + '.log\"' + \
                    ' -f null -'
                print(cmd)
                subprocess.Popen(cmd, shell=True)
                time.sleep(0.01)

                cmd = 'ffmpeg ' + '-i ' + ref_path + ref_image + \
                    ' -i ' + test_path + test_image + \
                    ' -lavfi ssim=\"stats_file=' + test_path + 'ssim' + str(int(test_image.split(test_name_rule)[0])) + '.log\"' + \
                    ' -f null -'
                print(cmd)
                subprocess.Popen(cmd, shell=True)
                time.sleep(0.01)
                break

# check process
while check_proc('ffmpeg'):
    time.sleep(0.1)

# static metric
flog = open('metric.log', 'w')
log_file = [f for f in os.listdir(test_path)]

psnr_avg_a = []
psnr_avg_r = []
psnr_avg_g = []
psnr_avg_b = []
psnr_order = []

ssim_r = []
ssim_g = []
ssim_b = []
ssim_all = []
ssim_order = []


for log in log_file:
    if log.endswith('.log'):
        file = open(test_path + log, 'r')
        num, _ = log.split('.log')
        if 'psnr' in log:
            num= int(num.split('psnr')[1])
            line = file.readline()
            n, mse_avg, mse_r, mse_g, mse_b, psnr_avg, psnr_r, psnr_g, psnr_b, _ = line.split(' ')
            # print(psnr_avg, psnr_r, psnr_g, psnr_b)
            # flog.write(str(num) + ': ' + psnr_avg + ' ' +  psnr_r + ' ' + psnr_g + ' ' + psnr_b + '\n')
            #print('{:0>2d}'.format(num))
            #flog.write('{:0>2d}'.format(num) + ': ' + psnr_avg + ' ' +  psnr_r + ' ' + psnr_g + ' ' + psnr_b + '\n' )
            #print(psnr_avg.split('psnr_avg:')[1])
            psnr_avg_a.append(float(psnr_avg.split('psnr_avg:')[1]))
            psnr_avg_r.append(float(psnr_r.split('psnr_r:')[1]))
            psnr_avg_g.append(float(psnr_g.split('psnr_g:')[1]))
            psnr_avg_b.append(float(psnr_b.split('psnr_b:')[1]))
            psnr_order.append(num)
        if 'ssim' in log:
            num= int(num.split('ssim')[1])
            line = file.readline()
            n, R, G, B, ALL, _ = line.split(' ')
            # print(psnr_avg, psnr_r, psnr_g, psnr_b)
            # flog.write(str(num) + ': ' + psnr_avg + ' ' +  psnr_r + ' ' + psnr_g + ' ' + psnr_b + '\n')
            #print('{:0>2d}'.format(num))
            #flog.write('{:0>2d}'.format(num) + ': ' + psnr_avg + ' ' +  psnr_r + ' ' + psnr_g + ' ' + psnr_b + '\n' )
            #print(psnr_avg.split('psnr_avg:')[1])
            ssim_all.append(float(ALL.split('All:')[1]))
            ssim_r.append(float(R.split('R:')[1]))
            ssim_g.append(float(G.split('G:')[1]))
            ssim_b.append(float(B.split('B:')[1]))
            ssim_order.append(num)
        os.remove(test_path + log)

for i in range(1, len(ssim_order) + 1):
    psnr_index = psnr_order.index(i)
    ssim_index = ssim_order.index(i)
    # flog.write( '{:0>2d}'.format(i) + \
    #             'psnr_avg:' +  '{:.2f}'.format(psnr_avg_a[psnr_index]) + ' ' + \
    #             'psnr_r: ' +  '{:.2f}'.format(psnr_avg_r[psnr_index]) + ' ' + \
    #             'psnr_g: ' +  '{:.2f}'.format(psnr_avg_g[psnr_index]) + ' ' + \
    #             'psnr_b: ' +  '{:.2f}'.format(psnr_avg_b[psnr_index]) + ' ' + \
    #             'ssim_avg:' +  '{:.4f}'.format(ssim_all[ssim_index]) + ' ' + \
    #             'ssim_r: ' +  '{:.4f}'.format(ssim_all[ssim_index]) + ' ' + \
    #             'ssim_g: ' +  '{:.4f}'.format(ssim_all[ssim_index]) + ' ' + \
    #             'ssim_b: ' +  '{:.4f}'.format(ssim_all[ssim_index]) + ' ' + \
    #                 '\n')
    flog.write( '{:0>2d}'.format(i) + '  '\
                'psnr:' +  '{:.2f}'.format(psnr_avg_a[psnr_index]) + ' ' + \
                'ssim:' +  '{:.6f}'.format(ssim_all[ssim_index]) + ' ' + \
                    '\n')

flog.write('\n')
flog.write('Summry: \n')
#flog.write('psnr:' +  '{:.2f}'.format(np.mean(psnr_avg_a)) + ' ' + 'psnr_r: ' +  '{:.2f}'.format(np.mean(psnr_avg_r)) + ' ' + 'psnr_g: ' +  '{:.2f}'.format(np.mean(psnr_avg_g)) + ' ' + 'psnr_b: ' +  '{:.2f}'.format(np.mean(psnr_avg_b)) + '\n')
flog.write('psnr:' +  '{:.2f}'.format(np.mean(psnr_avg_a)) + ' ' + 'ssim:' + '{:.6f}'.format(np.mean(ssim_all)))
flog.close()
shutil.move('metric.log', test_path + 'metric.log')

