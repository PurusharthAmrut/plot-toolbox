import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from colors import colors
import numpy as np
from config import *
from os.path import join

axes_label_font_size = None

def getBaseline(read_path):
    return pd.read_csv(read_path, delimiter='  ', engine='python', usecols=['X','CD_Signal']).iloc[::-1].reset_index(drop=True)

def getAbsorption(read_path):
    return pd.read_csv(read_path)

def setup_params():

    global axes_label_font_size
    axes_label_font_size = 20
    x_ticks_font_size = 20

    updates = {
        'font.size':12,
        'mathtext.default':'regular',
    }
    plt.rcParams.update(updates)
    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    plt.xticks(fontsize=x_ticks_font_size)
    plt.yticks(fontsize=x_ticks_font_size)

def plot_CD_from_file_list(read_path, start_x=350, end_x=550):

    df_baseline = getBaseline(baseline_path)

    xticks_interval = 10
    
    fname_list_ptr = open(read_path,'r')

    i = 0
    skip_flag = False
    for fname in fname_list_ptr.readlines():
        fname = fname.strip()

        if fname == '':
            # Empty line resets skip flag
            skip_flag = False
            continue

        elif skip_flag:
            continue

        elif fname[0] == '#':
            # comment line
            continue

        elif fname[0] == '%':
            skip_flag = True
            continue

        else:
            flabel = fname.split(' ')[0].split('_')
            film_num = flabel[2][4:]
            if len(flabel) == 4:
                angle = flabel[3]
            elif len(flabel) == 5:
                angle = flabel[3]+'_'+flabel[4]
            else:
                print("Invalid file label")
                return

        line_label = 'film-'+film_num+' '+angle

        df = pd.read_csv(join(cd_data_dir_path,fname), delimiter='  ', engine='python', usecols=['X','CD_Signal']).iloc[::-1].reset_index(drop=True)

        plt.plot(df['X'],df['CD_Signal']-df_baseline['CD_Signal'], label=line_label, color=colors[int(i%5)])
    
        i = i+1

    x_ticks = np.arange(start_x,end_x+1,xticks_interval)
    
    plt.xlim([start_x,end_x])
  
    plt.xticks(x_ticks,[str(num) if (num-start_x)%20==0 else '' for num in x_ticks])

    setup_params()
    plt.ylabel('CD', fontsize=axes_label_font_size)
    plt.xlabel('Wavelength (nm)', fontsize=axes_label_font_size)
    plt.legend()
    plt.show()

def plot_gCD_from_file_list(read_path, start_x=350, end_x=498):
    '''Uncomment all required films in file_list.txt before using this function'''

    df_baseline = getBaseline(baseline_path)
    df_abs = getAbsorption(abs_data_path)

    xticks_interval = 10

    cutoff = 550-end_x
    
    fname_list_ptr = open(read_path,'r')
    CD_df_list = list()
    g_CD_list = dict()

    i = 0
    skip_flag = False
    for fname in fname_list_ptr.readlines():
        fname = fname.strip()

        if fname == '':
            # Empty line resets skip flag
            skip_flag = False
            continue

        elif skip_flag:
            continue

        elif fname[0] == '#':
            # comment line
            continue

        elif fname[0] == '%':
            skip_flag = True
            continue

        flabel = fname.split(' ')[0].split('_')
        film_num = flabel[2][4:]
        film_label = 'film '+film_num
        if len(flabel)!=4:
            if len(flabel)==5:
                # Skip this file since it is the flipped film measurement
                continue
            else:
                print("Invalid file label")
                return

        if int(film_num) in [1,2]:
            uv_column = df_abs.columns.values[int(film_num)]
        elif int(film_num) in [4,5]:
            uv_column = df_abs.columns.values[int(film_num)-1]
        df = pd .read_csv(join(cd_data_dir_path,fname), delimiter='  ', engine='python', usecols=['X','CD_Signal']).iloc[::-1].reset_index(drop=True)
        CD_df_list.append(df)
        if i%4==3:
            if len(CD_df_list)!=4:
                print('Unexpected number of files to calculate g_CD...')
                return
            cd_avg = (CD_df_list[0]['CD_Signal']+CD_df_list[1]['CD_Signal']+CD_df_list[2]['CD_Signal']+CD_df_list[3]['CD_Signal'])/4
            g_CD = ((cd_avg-df_baseline['CD_Signal'])/df_abs[uv_column])/3300
            plt.plot(CD_df_list[0]['X'][:-cutoff],g_CD[:-cutoff], label=film_label)

            g_CD_list[film_label] = g_CD[:-cutoff].max()
            CD_df_list = list()

        i = i+1

    print(g_CD_list)

    x_ticks = np.arange(start_x,end_x+1,xticks_interval)

    plt.xlim([start_x,end_x])
    plt.xticks(x_ticks,[str(num) if (num-start_x)%20==0 else '' for num in x_ticks])

    setup_params()
    plt.xlabel('Wavelength (nm)', fontsize=axes_label_font_size)
    plt.ylabel('$g_{CD}$', fontsize=axes_label_font_size)
    plt.legend()
    plt.show()

plot_gCD_from_file_list(cd_files_list_path)