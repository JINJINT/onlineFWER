import numpy as np
from spending_FWER import *
from adaptive_spending_FWER import *
from discarding_spending_FWER import *
from adaptive_discarding_spending_FWER import *
from adaptive_discarding_spending_lodep_FWER import *

from saving_FWER import *
from discarding_saving_FWER import *

from sidak_FWER import *
from adaptive_sidak_FWER import *
from discarding_sidak_FWER import *
from adaptive_discarding_sidak_FWER import *

from recycling_FWER import *

import os
import scipy.optimize as optim
from scipy.stats import norm
from scipy.stats import bernoulli

from generatePvalue import *
from toimport import *
from generateHPY import *


################ Running entire framework  ####################

def run_single(non_range, NUMRUN, NUMHPY, NUMDRAWS, mu_N, mu_A, tau, lbd, pi, alpha0, markov_lag, FWER_proc, gamma_vec_exponent=2, two_sided = False, sigma = 1, verbose = False, rndseed = 0):

    if non_range < pi:
        raiseError(ValueError,'the range of non-nulls should not be smaller than pi')


    Hypo = get_hyp(pi, NUMHPY, non_range)
    Hypo = Hypo.astype(int)
    num_alt = np.sum(Hypo)
       
    dir_name = './dat'
    if two_sided:
        filename = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided_NR%d' % (mu_N, mu_A, tau, lbd, sigma, FWER_proc, NUMHPY, NUMDRAWS, markov_lag, non_range, pi, alpha0,gamma_vec_exponent, NUMRUN)
    else:
        filename = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided_NR%d' % (mu_N, mu_A, tau, lbd, sigma, FWER_proc, NUMHPY, NUMDRAWS, markov_lag, non_range, pi, alpha0, gamma_vec_exponent, NUMRUN)

    # ----------- initialize result vectors and mats ------------- ##
    pval_mat = np.zeros([NUMHPY, NUMRUN]) 
    rej_mat = np.zeros([NUMHPY, NUMRUN])
    alpha_mat = np.zeros([NUMHPY, NUMRUN])
    falrej_vec = np.zeros(NUMRUN) 
    falrej_mat = np.zeros([NUMHPY, NUMRUN]) 
    correj_vec = np.zeros(NUMRUN)
    correj_mat = np.zeros([NUMHPY, NUMRUN])    
    totrej_vec = np.zeros(NUMRUN)
    TDR_vec = np.zeros(NUMRUN)        
    FWER_vec = np.zeros(NUMRUN)
    FWER_mat = np.zeros([NUMHPY, NUMRUN])

    # ----------------- Run experiments ------------------ # 
    for l in range(NUMRUN):

        #Some random seed
        if rndseed == 1:
            rndsd = l+50
        else:
            rndsd = None

        # Create a vector of  different mu gaps
        muA = np.ones(NUMHPY)*mu_A
        this_exp = row_exp_new_batch(NUMHPY, NUMDRAWS, Hypo, mu_N, mu_A, markov_lag, two_sided, sigma) 


        #%%%%%%%%% Run experiments: Get sample and p-values etc. %%%%%%%%%%%%%
        # Generate p-value from mu-vec, with same random seed 
        this_exp.gauss_two_mix(markov_lag, rndsd)
        pval_mat[:, l] = this_exp.pvec
        

        # Initialize FWER_proc
        if FWER_proc == 1: # ADDIS-Spending
            proc = adaptive_discarding_spending_proc(alpha0, NUMHPY, gamma_vec_exponent, tau, lbd, markov_lag)
        elif FWER_proc == 2: # Adaptive-Spending
            proc = adaptive_spending_proc(alpha0, NUMHPY, gamma_vec_exponent, lbd, markov_lag)
        elif FWER_proc == 3: # Discard-Spending
            proc = discarding_spending_proc(alpha0, NUMHPY, gamma_vec_exponent, tau, markov_lag)
        elif FWER_proc == 4: # Alpha-Spending
            proc = spending_proc(alpha0, NUMHPY, gamma_vec_exponent, markov_lag)
        elif FWER_proc == 5: # ADDIS -Spending with local dependence
            proc = adaptive_discarding_spending_lodep_proc(alpha0, NUMHPY, gamma_vec_exponent, tau, lbd, markov_lag)
        elif FWER_proc == 6: # Online Fallback-1
            proc = saving_proc(alpha0, NUMHPY, gamma_vec_exponent) 
        elif FWER_proc == 7: # Discard Fallback-1                  
            proc = discarding_saving_proc(alpha0, NUMHPY, gamma_vec_exponent, tau)
        elif FWER_proc == 8: # Online Sadik
            proc = sidak_proc(alpha0, NUMHPY, gamma_vec_exponent)
        elif FWER_proc == 9: # Adaptive Sadik 
            proc = adaptive_sidak_proc(alpha0, NUMHPY, gamma_vec_exponent, lbd)
        elif FWER_proc == 10: # Discard Sadik
            proc = discarding_sidak_proc(alpha0, NUMHPY, gamma_vec_exponent, tau) 
        elif FWER_proc == 11: # Addis Sadik
            proc = adaptive_discarding_sidak_proc(alpha0, NUMHPY, gamma_vec_exponent, tau, lbd)  
        elif FWER_proc == 12: # Online Fallback
            proc = recycling_proc(alpha0, NUMHPY, gamma_vec_exponent)              
   

        #%%%%%%%%%% Run FWER, get rejection and next alpha %%%%%%%%%%%%
        rej_mat[:, l] = proc.run_proc(this_exp.pvec)
        alpha_mat[:, l] = proc.alpha

        #%%%%%%%%%%  Save results %%%%%%%%%%%%%%
        falrej_singlerun = np.array(rej_mat[:,l])*np.array(1-Hypo)
        correj_singlerun = np.array(rej_mat[:,l])*np.array(Hypo)
        falrej_vec[l] = np.sum(falrej_singlerun)
        correj_vec[l] = np.sum(correj_singlerun)
        falrej_mat[:, l] = falrej_singlerun

        FWER_vec = np.zeros(NUMHPY)
        for j in range(NUMHPY):
            time_vec = np.arange(NUMHPY) < (j+1)
            FWER_vec[j] = np.sum(falrej_singlerun * time_vec)

        FWER_mat[:,l] = FWER_vec
        
    # -----------------  Compute average quantities we care about ------------- #

    TDR_vec = np.true_divide(correj_vec, num_alt) # power of each trial
    FWER_vec = [FWER_mat[NUMHPY - 1][l] for l in range(NUMRUN)] # FWER in the end

    if verbose == 1:
        print("done with computation")

    # Save data
    data = np.r_[np.expand_dims(TDR_vec, axis=0), np.expand_dims(np.asarray(FWER_vec),axis=0)]
    saveres(dir_name, filename, data)



