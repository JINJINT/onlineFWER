import numpy as np


class sidak_proc:

	def __init__(self, alpha0, numhpy, gamma_vec_exponent, markov_lag=0):
		self.alpha0 = alpha0 #FWER level
		self.alpha = np.zeros(numhpy) # alpha vec
		# Cmopute the discount gamma sequence and make it sum to one
		tmp = range(1, 10000)
		self.gamma_vec = np.true_divide(np.ones(len(tmp)), np.power(tmp, gamma_vec_exponent))
		self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))
 

	# Running Sidak on pvec
	def run_proc(self, pvec):
		numhpy = len(pvec)      	
		R = np.zeros(numhpy) # rejection vec

		for k in range(numhpy):
			self.alpha[k] =  1 - np.power(1 - self.alpha0, self.gamma_vec[k])
			if pvec[k] <= self.alpha[k]:
				R[k] = 1

		return R



