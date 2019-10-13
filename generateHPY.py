import numpy as np
np.set_printoptions(precision = 4)
from scipy.stats import bernoulli

from toimport import *


def get_hyp(pi1, num_hyp, non_range):
        
    # Read hyp from file
    if not os.path.exists('./expsettings'):
        os.makedirs('./expsettings')
    filename_pre = "H_PM%.2f_NH%d_R%.3f" % (pi1, num_hyp, non_range)
    hypo_filename = [filename for filename in os.listdir('./expsettings') if filename.startswith(filename_pre)]
    if len(hypo_filename) > 0:
        # Just take the first sample
        hyp_mat = np.loadtxt('./expsettings/%s' % hypo_filename[0])    
    else:
        print("Hyp file doesn't exist, thus generating the file now ...")
        # Generate 100 draws of num_hyp hypotheses with given pi_1 setting
        hyp_mat = generate_hyp(pi1, num_hyp, 100, non_range)
    Hypo = hyp_mat[0]
    
    return Hypo


def generate_hyp(pi1, max_hyp, samples, non_range):

    hyp_mat = np.zeros([samples, max_hyp])

    for i in range(samples):
        Hyp = np.array([])
        Hyp = np.concatenate((Hyp, bernoulli.rvs(pi1/non_range, size = int(max_hyp*non_range))))      
        Hyp = np.concatenate((Hyp, np.zeros((max_hyp-int(max_hyp*non_range),),dtype = np.int)))
        hyp_mat[i] = Hyp  

    # ----- Save sample hypotheses vectors ----- #
    dirname = './expsettings'
    filename = "H_PM%.2f_NH%d_R%.3f" % (pi1, max_hyp, non_range)
    saveres(dirname, filename, hyp_mat)
    
    return hyp_mat
    
        
        
