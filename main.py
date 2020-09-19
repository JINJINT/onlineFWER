import logging, argparse
import numpy as np
from computeFWER import *
from plottingresults import *
from toimport import *
from pathos.multiprocessing import ProcessingPool as Pool


def main():

    if not os.path.exists('./dat'):
        os.makedirs('./dat')

    #########%%%%%%  SET PARAMETERS FOR RUNNING EXPERIMENT %%%%%%%##########

    FWERrange = str2list(args.FWERrange)
    muNrange = str2list(args.mu_N, 'float')
    muArange = str2list(args.mu_A, 'float')
    sigma_N = 1
    plotstyle = str2list(args.plot_style)
    pirange = str2list(args.pirange, 'float') 
    mode = args.mode
    hyprange = [0] 
    non_ranges = args.non_range
    if mode ==2:
        non_ranges = "0.1, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26"
        pirange = str2list('0.1', 'float')
    if non_ranges == '':
        if mode == 0:
            non_ranges = np.ones(len(pirange))
        elif mode == 1:
            denser = (1+1/max(pirange))/2
            non_ranges = denser*np.array(pirange)
        elif mode == 2:
            non_ranges = pirange[0]*splitrange(1,1/pirange[0],9)
    else:
        non_ranges = np.array(str2list(non_ranges, 'float'))               
    non_range = [ round(elem, 3) for elem in non_ranges ]
    if len(pirange)!=len(non_range):
        for i in range(len(non_range)-len(pirange)):
            pirange.append(pirange[0]) 
    
    ########%%%%%%%%%%%%%%%%% RUN EXPERIMENT %%%%%%%%########################
    for mu_A in muArange:   
        def singlepi(i):
            for mu_N in muNrange:
                for FWER in FWERrange:
                    pi = pirange[i]
                    if args.two_sided:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_two_sided_NR%d' % (mu_N, mu_A, args.tau, args.lbd, sigma_N, FWER, args.num_hyp, 1, args.markov_lag, non_range[i], pi, args.alpha0, args.gamma, args.num_runs)
                    else:
                        filename_pre = 'MN%.2f_MA%.1f_tau%.2f_lbd%.2f_Si%.1f_FWER%d_NH%d_ND%d_L%d_R%.3f_PM%.2f_alpha0%.2f_gamma%.2f_one_sided_NR%d' % (mu_N, mu_A, args.tau, args.lbd, sigma_N, FWER, args.num_hyp, 1, args.markov_lag, non_range[i], pi, args.alpha0, args.gamma, args.num_runs)

                    all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]                

                    # Run experiment if data doesn't exist yet
                    if all_filenames == []:
                        print("Running experiment for FWER procedure %s and pi %.1f and muN %.1f  and muA %.1f and sigmaN %.1f with lag %d and alpha0 %.2f and tau %.2f and lbd %.2f and non_range %.3f and gamma_vec_exponent %.2f " % (proc_list[FWER-1], pi, mu_N, mu_A, sigma_N, args.markov_lag, args.alpha0, args.tau, args.lbd, non_range[i], args.gamma))
                        run_single(non_range[i], args.num_runs, args.num_hyp, 1, mu_N, mu_A, args.tau, args.lbd, pi, args.alpha0, args.markov_lag, FWER, args.gamma, args.two_sided, sigma_N)
                    else:
                        print("Experiments for FWER procedure %s and pi %.1f and muN %.1f and muA %.1f and sigmaN %.1f with lag %d and alpha0 %.2f and tau %.2f and lbd %.2f and non_range %.3f and gamma_vec_exponent %.2f are already run" % (proc_list[FWER-1], pi, mu_N, mu_A, sigma_N, args.markov_lag, args.alpha0, args.tau, args.lbd, non_range[i], args.gamma))
        with Pool() as p:
            TDR_vec = p.map(singlepi, range(len(pirange)))
            p.close()
            p.join()
            p.terminate()   
            p.restart() 

        # Plot different measures over hypotheses for different FWER
        print("Now plotting ... ")
        for style in plotstyle:
            plot_results(style, 0, FWERrange, pirange, non_range, hyprange, args.tau, args.lbd, muNrange, mu_A, sigma_N, args.num_hyp, args.num_runs, args.markov_lag, args.alpha0, mode, args.gamma, args.two_sided)      

'''
Algorithms:
1:'ADDIS-Spending'
2:'Adaptive-Spending'
3:'Discard-Spending'
4:'Alpha-Spending',
5:'ADDIS-Spending-lag'
6:'Online-Fallback-1'
7:'Discard-Fallback-1'
8:'Online Sidak',
9:'Adaptive-Sidak'
10:'Discard-Sidak'
11:'ADDIS-Sidak'
12:'Online-Fallback'
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--FWERrange', type=str, default = "1") # choice of algorithms
    parser.add_argument('--num-runs', type=int, default = 2000) # number of independent trials
    parser.add_argument('--num-hyp', type=int, default = 1000) # number of hypotheses
    parser.add_argument('--alpha0', type=float, default = 0.2) # FWER level
    parser.add_argument('--tau', type=float, default = 0.5) # discarding level
    parser.add_argument('--lbd', type=float, default = 0.5) # adaptive level    
    parser.add_argument('--mu-N', type=str, default = "-2") # mu_N for gaussian tests
    parser.add_argument('--mu-A', type=str, default = "4") # mu_A for gaussian tests
    #parser.add_argument('--sigma-N', type=float, default = 1) # sigma_N for gaussian test
    # parser.add_argument('--sigma-A', type=str, default = "2, 4") # sigma_A for gaussian test
    parser.add_argument('--two-sided', action = 'store_true') # mu_A for gaussian tests
    parser.add_argument('--gamma', type=float, default = 2) # the order of gamma sequence
    parser.add_argument('--pirange', type=str, default = '0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9') # range of pi_A
    parser.add_argument('--markov-lag', type=int, default = 0) # lag in the local dependence
    parser.add_argument('--mode', type = int, default = 0) # 0 for randomized sampling, 1 for sampling with denser pi_A, 2 for sampling with the same pi_A and different range  
    parser.add_argument('--non-range', type = str, default = "")
    parser.add_argument('--plot-style', type = str, default = "1") # 1 for plots with multiprocedure , 2 for plots with multiple mu-N
    args = parser.parse_args()
    logging.info(args)
    main()

##=== influence of alpha
# python main.py --alpha0 0.05
# python main.py --alpha0 0.1

##=== influence of gamma
# python main.py --gamma 1.01
# python main.py --gamma 1.5
# python main.py --gamma 5

##=== influence of lag
# python main.py --markov-lag 50
# python main.py --markov-lag 10


##=== influence of two-sided
# python main.py --two-sided







