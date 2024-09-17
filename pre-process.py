import re
from config import *
from os.path import join

file = open(pre_process_files_list_path,'r')

for fname in file.readlines():
    fname = fname.strip()

    if fname=='':
        break

    f_in = open(join(raw_data_dir_path, fname),'r')
    raw_input = f_in.read()
    f_in.close()

    start = re.search('X  CD_Signal', raw_input).start()
    end = re.search('[$]ENDDATA',raw_input).start()

    f_out = open(join(cd_data_dir_path, fname[:-3]+'csv'),'w')
    f_out.write(raw_input[start:end])
    f_out.close()

print('Pre-processing completed...')