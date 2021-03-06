import numpy as np


class discarding_sidak_proc:

	def __init__(self, alpha0, numhpy, gamma_vec_exponent, tau, markov_lag=0):
		self.alpha0 = alpha0 #FWER level
		self.alpha = np.zeros(numhpy) # alpha vec
		self.tau = tau
		# Cmopute the discount gamma sequence and make it sum to one
		tmp = range(1, 10000)
		self.gamma_vec = np.true_divide(np.ones(len(tmp)), np.power(tmp, gamma_vec_exponent))
		self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))
 

	def run_proc(self, pvec):
		numhpy = len(pvec)      	
		S = np.zeros(numhpy) # choosen vec
		R = np.zeros(numhpy) # rejection vec

		for k in range(numhpy):
			if pvec[k]<=self.tau:
				S[k] = 1
			beta = self.tau * self.gamma_vec[int(sum(S[:(k+1)])-1)]
			self.alpha[k] =  1 - np.power(1 - self.alpha0, beta)
			if pvec[k] <= self.alpha[k]:
				R[k] = 1

		return R


