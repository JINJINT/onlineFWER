import numpy as np
from numpy import sqrt, log, exp, mean, cumsum, sum, zeros, ones, argsort, argmin, argmax, array, maximum, concatenate
from numpy.random import randn, rand
np.set_printoptions(precision = 10)
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 24
mpl.rcParams['axes.labelsize'] = 28
mpl.rcParams['xtick.labelsize']= 20
mpl.rcParams['ytick.labelsize']= 20

import matplotlib.pyplot as plt
plt.switch_backend('agg')
pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)

## Plotting settings
colordic = {'ADDIS-Spending': 'green',
            'Adaptive-Spending': 'darkorange',
            'Discard-Spending':'royalblue',
            'Alpha-Spending': 'firebrick',  
            'ADDIS-Spending-lag': 'green',
            'Online Fallback-1': 'm',
            'Discard Fallback-1': 'royalblue',
            'Online Sidak': 'saddlebrown',
            'Adaptive-Sidak ': 'darkorange',
            'Discard-Sidak': 'royalblue',
            'ADDIS-Sidak': 'green', 
            'Online Fallback': 'purple'}

plot_style = ['-', '--','-.',':','--']
plot_col = ['gold', 'orange', 'darkorange','orangered']
plot_mark = [ 'x', 'o', 'v', '^', 'D', '+']



def saveplot(direc, filename, lgd, ext = 'pdf',  close = True, verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    plt.savefig(savepath, bbox_extra_artists=(lgd,), bbox_inches='tight')
    if verbose:
        print("Saving figure to %s" % savepath)
    if close:
        plt.close()


def plot_errors_mat_both(xs, matrix_av_pow, matrix_av_fwer, matrix_err_pow, matrix_err_fwer, labels, dirname, filename, xlabel, ylabel, col = True):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    no_lines = len(matrix_av_pow)

    for i in range(no_lines):
            ys = np.array(matrix_av_pow[i])
            zs = np.array(matrix_err_pow[i])
            if col:
                color = colordic[labels[i]]
            else:
                color = plot_col[i]    
            ax.errorbar(xs, ys, yerr = zs, color = color, marker = plot_mark[i % len(plot_mark)], linestyle = plot_style[i%len(plot_style)], lw = 2, markersize = 5, label = labels[i])
    #lgd = ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, handletextpad=0.3,
    #            ncol=min(no_lines,2), mode="expand", borderaxespad=0., prop={'size': 10})

    for j in range(no_lines):
            ys = np.array(matrix_av_fwer[j])
            zs = np.array(matrix_err_fwer[j])
            if col:
                color = colordic[labels[j]]
            else:
                color = plot_col[j]  
            ax.errorbar(xs, ys, yerr = zs, color = color, marker = plot_mark[j % len(plot_mark)], linestyle = plot_style[j%len(plot_style)], lw= 2, markersize = 5, label = None, alpha = 0.7)
    
    ax.hlines(y=0.2, xmin=min(xs), xmax = max(xs), color='k', lw =3)
    ax.set_xlabel(xlabel, labelpad=15)
    ax.set_ylabel(ylabel, labelpad=15)
    ax.set_ylim((0, 1))
    ax.set_xlim((min(xs), max(xs)))
    yt = ax.get_yticks() 
    yt[0] = 0.2
    yt = np.round(yt,1)
    ytl = yt.tolist()
    ytl[0] = "0.2"
    ax.set_yticks(yt)
    ax.set_yticklabels(ytl)
    ax.grid(True)
    saveplot(dirname, filename, ax)


