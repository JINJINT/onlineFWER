### Import Python libraries
import numpy as np
np.set_printoptions(precision = 4)
import sys

### Import utilities for plotting
from ploting import*
from generateHPY import*
from toimport import*


def plot_results(plot_style, whichrun, FWERrange, pirange, non_range, hyprange, tau, lbd, muNrange, mu_A, sigma, NUMHYP, num_runs, markov_lag, alpha0, mode,gamma = 2, two_sided=False, NUMDRAWS = 1):

    plot_dirname = './plots'
    
    ############# FWER of same proc with different mu_N parameters ##########

    if plot_style == 1:

        FWERstr = list2str(FWERrange)
        legends_list = np.array(proc_list).take([t-1 for t in FWERrange]) 

        for mu_N in muNrange:
            TDR_av = []
            TDR_std = []
            FWER_av = []
            FWER_std = []
            ind = 0
            
            for index, FWER in enumerate(FWERrange):
        
                all_filenames = []

                for d, non_ran in enumerate(non_range):
                    if two_sided:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided' % (mu_N, mu_A, tau, lbd, sigma, FWER, NUMHYP, NUMDRAWS, markov_lag, non_ran, pirange[d], alpha0, gamma)
                    else:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided' % (mu_N, mu_A, tau, lbd, sigma, FWER, NUMHYP, NUMDRAWS, markov_lag, non_ran, pirange[d], alpha0, gamma)

                    filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]
                    if all_filenames == []:
                        all_filenames = filenames
                    else:
                        for file in filenames:
                            all_filenames.append(file)   

                if all_filenames == []:
                    print("No file found!")
                    print(filename_pre)
                    sys.exit()

                # Get values of  pi s from the file name
                pos_PM_start = [all_filenames[i].index('PM') for i in range(len(all_filenames))]
                pos_PM_end = [all_filenames[i].index('_al') for i in range(len(all_filenames))]
                PM_vec = [float(all_filenames[i][pos_PM_start[i] + 2:pos_PM_end[i]]) for i in range(len(all_filenames))]

                # Get values of  non_range s from the file name
                pos_ran_start = [all_filenames[i].index('_R') for i in range(len(all_filenames))]
                pos_ran_end = [all_filenames[i].index('_PM') for i in range(len(all_filenames))]
                ran_vec = [float(all_filenames[i][pos_ran_start[i] + 2:pos_ran_end[i]]) for i in range(len(all_filenames))]
                       
                if mode == 0 or mode == 1:
                    xs_list = pirange
                    xs_vec = PM_vec
                
                elif mode == 2:
                    xs_list = non_range
                    xs_vec = ran_vec

                # Initialize result matrices
                TDR_av.append(np.zeros([1, len(xs_list)]))
                TDR_std.append(np.zeros([1, len(xs_list)]))
                FWER_av.append(np.zeros([1, len(xs_list)]))
                FWER_std.append(np.zeros([1, len(xs_list)]))
                TDR_std.append(np.zeros([1, len(xs_list)]))
                TDR_vec = np.zeros(len(xs_list))
                FWER_vec = np.zeros(len(xs_list))               
                TDR_vec_std = np.zeros(len(xs_list))
                FWER_vec_std = np.zeros(len(xs_list))

                # # Merge everything with the same NA and NH
                for k, xs in enumerate(xs_list):
                    indices = np.where(np.array(xs_vec) == xs)[0]
                    result_mat = []
                    # Load resultmats and append
                    for j, idx in enumerate(indices):
                        result_mat_cache = np.loadtxt('./dat/%s' % all_filenames[idx])
                        result_mat_cache = result_mat_cache[-2:, 0:num_runs] # TDR_vec and FWER_vec, default run numbers
                        if (j == 0):
                            result_mat = result_mat_cache
                        else:
                            result_mat = np.c_[result_mat, result_mat_cache]

                    numrun = len(result_mat[0])
                    TDR_vec[k] = np.average(result_mat[0])
                    TDR_vec_std[k] = np.true_divide(np.std(result_mat[0]),np.sqrt(numrun))
                    FWER_vec[k] = np.average(result_mat[1]>0)
                    FWER_vec_std[k] = np.true_divide(np.std(result_mat[1]>0), np.sqrt(numrun))                   
                TDR_av[ind] = [TDR_vec[k] for k in range(len(xs_list))]
                TDR_std[ind] = [TDR_vec_std[k] for k in range(len(xs_list))]
                FWER_av[ind] = [FWER_vec[k] for k in range(len(xs_list))]
                FWER_std[ind] = [FWER_vec_std[k] for k in range(len(xs_list))]              
                ind = ind + 1


            # -------- PLOT ---------------
            xs = xs_list
            if mode == 0:
                x_label = '$\pi_A$'
                extra_info = ""
            if mode == 1:
                x_label = 'e'
                extra_info = ""   
            elif mode == 2:
                x_label = 'C'
                extra_info = str(PM_vec[0])             
            
            if two_sided:    
                filename = 'PowFWERvsPI_FWER%s_MN%.2f_MA%.1f_Si%.1f_NH%d_ND%d_L%d_MOD%d_gamma%.2f_two_sided_%s' %  (FWERstr, mu_N, mu_A, sigma, NUMHYP, NUMDRAWS, markov_lag, mode, gamma, extra_info)
            else:
                 filename = 'PowFWERvsPI_FWER%s_MN%.2f_MA%.1f_Si%.1f_NH%d_ND%d_L%d_MOD%d_gamma%.2f_one_sided_%s' %  (FWERstr, mu_N, mu_A, sigma, NUMHYP, NUMDRAWS, markov_lag, mode, gamma, extra_info)

            plot_errors_mat_both(xs, TDR_av, FWER_av, TDR_std, FWER_std, legends_list, plot_dirname, filename, x_label, 'FWER / Power')


    ############# FWER of same proc with different mu_N parameters ##########

    elif plot_style == 2:
        
        for index, FWER in enumerate(FWERrange):
            muNstr = list2str(muNrange)
            legends_list = np.array(proc_list).take([t-1 for t in FWERrange])              
            muN_list = np.array(['$\mu_N$ = '+str(mu_N) for mu_N in muNrange])
            TDR_av = []
            TDR_std = []
            FWER_av = []
            FWER_std = []
            ind = 0
            for mu_N in muNrange:
            
                all_filenames = []
                for d, non_ran in enumerate(non_range):
                    if two_sided:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided' % (mu_N, mu_A, tau, lbd, sigma, FWER, NUMHYP, NUMDRAWS, markov_lag, non_ran, pirange[d], alpha0, gamma)
                    else:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided' % (mu_N, mu_A, tau, lbd, sigma, FWER, NUMHYP, NUMDRAWS, markov_lag, non_ran, pirange[d], alpha0, gamma)

                    filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]
                    if all_filenames == []:
                        all_filenames = filenames
                    else:
                        for file in filenames:
                            all_filenames.append(file)   

                if all_filenames == []:
                    print("No file found!")
                    print(filename_pre)
                    sys.exit()

                # Get values of  pi s from the file name
                pos_PM_start = [all_filenames[i].index('PM') for i in range(len(all_filenames))]
                pos_PM_end = [all_filenames[i].index('_al') for i in range(len(all_filenames))]
                PM_vec = [float(all_filenames[i][pos_PM_start[i] + 2:pos_PM_end[i]]) for i in range(len(all_filenames))]

                # Get values of  non_range s from the file name
                pos_ran_start = [all_filenames[i].index('_R') for i in range(len(all_filenames))]
                pos_ran_end = [all_filenames[i].index('_PM') for i in range(len(all_filenames))]
                ran_vec = [float(all_filenames[i][pos_ran_start[i] + 2:pos_ran_end[i]]) for i in range(len(all_filenames))]
                       
                if mode == 0 or mode == 1:
                    xs_list = pirange
                    xs_vec = PM_vec
                
                elif mode == 2:
                    xs_list = non_range
                    xs_vec = ran_vec

                # Initialize result matrices
                TDR_av.append(np.zeros([1, len(xs_list)]))
                TDR_std.append(np.zeros([1, len(xs_list)]))
                FWER_av.append(np.zeros([1, len(xs_list)]))
                FWER_std.append(np.zeros([1, len(xs_list)]))
                TDR_std.append(np.zeros([1, len(xs_list)]))
                TDR_vec = np.zeros(len(xs_list))
                FWER_vec = np.zeros(len(xs_list))              
                TDR_vec_std = np.zeros(len(xs_list))
                FWER_vec_std = np.zeros(len(xs_list))

                # Merge everything with the same NA and NH
                for k, xs in enumerate(xs_list):
                    indices = np.where(np.array(xs_vec) == xs)[0]
                    result_mat = []
                    # Load resultmats and append
                    for j, idx in enumerate(indices):
                        result_mat_cache = np.loadtxt('./dat/%s' % all_filenames[idx])
                        result_mat_cache = result_mat_cache[-2:, 0:num_runs] # TDR_vec and FWER_vec, default run numbers
                        if (j == 0):
                            result_mat = result_mat_cache
                        else:
                            result_mat = np.c_[result_mat, result_mat_cache]

                    numrun = len(result_mat[0])
                    TDR_vec[k] = np.average(result_mat[0])
                    TDR_vec_std[k] = np.true_divide(np.std(result_mat[0]),np.sqrt(numrun))
                    FWER_vec[k] = np.average(result_mat[1]>0)
                    FWER_vec_std[k] = np.true_divide(np.std(result_mat[1]>0), np.sqrt(numrun))                    
                TDR_av[ind] = [TDR_vec[k] for k in range(len(xs_list))]
                TDR_std[ind] = [TDR_vec_std[k] for k in range(len(xs_list))]
                FWER_av[ind] = [FWER_vec[k] for k in range(len(xs_list))]
                FWER_std[ind] = [FWER_vec_std[k] for k in range(len(xs_list))]               
                ind = ind + 1


            # -------- PLOT ---------------
            xs = xs_list 
            if mode == 0:
                x_label = '$\pi_A$'
                extra_info = ""
            if mode == 1:
                x_label = 'e'
                extra_info = ""           
            elif mode == 2:
                x_label = 'C'
                extra_info = str(PM_vec[0])


            ##### FWER vs pi #####
            if two_sided:    
                filename = 'PowFWERvsPI_FWER%s_MN%.2f_MA%.1f_Si%.1f_NH%d_ND%d_L%d_MOD%d_gamma%.2f_two_sided_%s' %  (FWER, muNstr, mu_A, sigma, NUMHYP, NUMDRAWS, markov_lag, mode, gamma, extra_info)
            else:
                 filename = 'PowFWERvsPI_FWER%s_MN%.2f_MA%.1f_Si%.1f_NH%d_ND%d_L%d_MOD%d_gamma%.2f_one_sided_%s' %  (FWER, muNstr, mu_A, sigma, NUMHYP, NUMDRAWS, markov_lag, mode, gamma, extra_info)

            plot_errors_mat_both(xs, TDR_av, FWER_av, TDR_std, FWER_std, muN_list, plot_dirname, filename, x_label, 'FWER / Power')




