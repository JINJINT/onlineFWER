### Import Python libraries
import numpy as np
np.set_printoptions(precision = 4)
import sys
import logging, argparse
### Import utilities for plotting
from ploting import*
from generateHPY import*
from toimport import*


def plot_best(pi, muN, muA, FWER, two_sided = False):

    plot_dirname = './plots' 

    taulist = np.round(np.arange(0.05, 1, 0.05),2)[::-1]
    lbdlist = np.round(np.arange(0.05, 1, 0.05),2)
                 
    TDR_av = np.zeros((len(taulist), len(lbdlist)))
    TDR_gap_av = np.zeros((len(taulist), len(lbdlist)))
    FWER_av = np.zeros((len(taulist), len(lbdlist)))
    FWER_bench_av = np.zeros((len(taulist), len(lbdlist)))

    print("extracting data ")
    for i, tau in enumerate(taulist):
        for j, lbd in enumerate(lbdlist):
            if two_sided:
                filename = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided_NR2000.dat' % (muN, muA, tau, lbd, 1, FWER, 1000, 1, 0, 1, pi, 0.2, 2)
            else:
                filename = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided_NR2000.dat' % (muN, muA, tau, lbd, 1, FWER, 1000, 1, 0, 1, pi, 0.2, 2)

            result_mat = np.loadtxt('./dat/%s' % filename)
            result_mat = result_mat[-2:, 0:2000] # TDR_vec and FWER_vec, default run numbers
            
            if two_sided:
                filename_bench = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER4_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided_NR2000.dat' % (muN, muA, tau, lbd, 1, 1000, 1, 0, 1, pi, 0.2, 2)
            else:
                filename_bench = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER4_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided_NR2000.dat' % (muN, muA, tau, lbd, 1, 1000, 1, 0, 1, pi, 0.2, 2)
            bench_mat = np.loadtxt('./dat/%s' % filename_bench)
            bench_mat = bench_mat[-2:, 0:2000] # TDR_vec and FWER_vec, default run numbers
            
            numrun = len(result_mat[0])
            TDR_av[i,j] = np.average(result_mat[0])
            TDR_gap_av[i,j] = np.average(result_mat[0] - bench_mat[0])
            FWER_av[i,j] = np.average(result_mat[1]>0)
            FWER_bench_av[i,j] = np.average(bench_mat[1]>0)

            print("finished the calculation for computing the power with muN %.2f and muA %.2f, and lbd %.3f and tau %.3f " %(muN, muA, lbd, tau))


    # # -------- PLOT ---------------
    # filenameexp = 'heatmap_tradeoff_MN%.1f_MA%.1f_pi%.1f_FWER%d' %  (muN, muA, pi, FWER)
   
    # # the heatmap of empirical power
    # heatmapplot("$\\theta$", "$\\tau$", TDR_av, plot_dirname, filenameexp, lbdlist, taulist, 0.2, 1, "") 

    # # the heatmap of empirical power gap
    # heatmapplot("$\\theta$", "$\\tau$", TDR_gap_av, plot_dirname, filenameexp, lbdlist, taulist, 0, 1, "gap") 

    # # the heatmap of empirical FWER
    # heatmapplot("$\\theta$", "$\\tau$", FWER_av, plot_dirname, filenameexp, lbdlist, taulist, 0, 0.2, "FWER") 

    # # the heatmap of empirical FWER bench
    # heatmapplot("$\\theta$", "$\\tau$", FWER_bench_av, plot_dirname, filenameexp, lbdlist, taulist, 0, 0.2, "FWERbench") 




def main():
    for pi in np.arange(0.1,1,0.4):
        plot_best(pi, -2, 4, 1, two_sided = False)
        plot_best(pi, -1, 4, 1, two_sided = False)
        plot_best(pi, 0, 4, 1, two_sided = False)
        #plot_best(pi, 0, 4, 1, two_sided = False)
 

if __name__ == "__main__":
    main()













