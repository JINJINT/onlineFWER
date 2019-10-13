import numpy as np
import os
from math import floor

proc_list = ['ADDIS-Spending','Adaptive-Spending','Discard-Spending','Alpha-Spending',
             'ADDIS-Spending-lag','Online Fallback-1','Discard Fallback-1','Online Sidak',
             'Adaptive-Sidak ','Discard-Sidak','ADDIS-Sidak', 'Online Fallback']

def saveres(direc, filename, mat, ext = 'dat', verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    np.savetxt(savepath, mat, fmt='%.3e', delimiter ='\t')
    if verbose:
        print("Saving results to %s" % savepath)
    
def str2list(string, type = 'int'):
    str_arr =  string.split(',')
    if type == 'int':
        str_list = [int(char) for char in str_arr]
    elif type == 'float':
        str_list = [float(char) for char in str_arr]
    return str_list


def list2str(lists):
    string = ''
    for i in lists:
        string = string + str(i)
    return string        

def splitrange(start, stop, size, by = 0):
    if by==0:
        range_list = np.array([start + i * (stop - start)/(size+1) for i in range(1,size+1)])
    else:
        size = floor((stop - start)/by)
        range_list = np.array([start + i*by for i in range(1,size)])
    return range_list



    