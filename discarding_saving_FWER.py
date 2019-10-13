import numpy as np

class discarding_saving_proc:

	def __init__(self, alpha0, numhpy, gamma_vec_exponent, tau, markov_lag=0):
		self.alpha0 = alpha0 #FWER level
		self.tau = tau # discarding threshold tau
		self.alpha = np.zeros(numhpy) # alpha vec
		self.markov_lag = markov_lag
		# Cmopute the discount gamma sequence and make it sum to one
		tmp = range(1, 10000)
		self.gamma_vec = np.true_divide(np.ones(len(tmp)), np.power(tmp, gamma_vec_exponent))
		self.gamma_vec = self.alpha0*self.gamma_vec / np.float(sum(self.gamma_vec))
        

	def run_proc(self, pvec):
		numhpy = len(pvec)
		S = np.zeros(numhpy) # choosen vec        	
		R = np.zeros(numhpy) # rejection vec
		T = np.zeros(numhpy) # the last tested position before moment k

		for k in range(numhpy):
			if pvec[k]<=self.tau:
				S[k] = 1
				T[k+1:] = k
			if k==0:
				self.alpha[k] = min(self.tau*self.gamma_vec[int(sum(S[:(k+1)])-1)], S[k])
			else:
				self.alpha[k] = min(self.tau*self.gamma_vec[int(sum(S[:(k+1)])-1)] + self.tau*self.alpha[int(T[k])]*R[int(T[k])], S[k])	
			if pvec[k]<=self.alpha[k]:
				R[k] = 1

		return R



		