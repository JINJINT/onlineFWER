This repository contains code of a series of new algorithms for online FWER control. 
It also contains code for reproducing all the figures in the corresponding paper.

====================================Common guidance ========================================

The main file is main.py. The experiments vary depending on the following passed arguments:  

#----------Common parameters  
 
FWERrange - integers encoding the choice of algorithms (listed in the comments of main.py)  

num-runs - number of independent trials  

num-hyp - number of hypotheses  

alpha0 - test level  

tau - the list of value of tau paired with the value of pi_A  

lbd - the list of value of lbd paired with the value of pi_A  

mu-N - used for gaussian tests as mu_N, where observations under the alternative are N(Z,1), Z~N(mu_N,1)  

mu-A - used for gaussian tests as mu_A, where observations under the alternative are N(Z,1), Z~N(mu_A,1)  

pirange - list of value of pi_A  

markov-lag - the lag length in local dependence

mode - the pattern of arriving of non-nulls

plot-style - the way to arrange plotting results

**************************************************************************************************************************  


========================== To reproduce the figures in the paper ==========================   

Run the following command in the terminal under the repository of current code repository  

Plots saved as .pdf files in the folder "plots", data saved as .dat files in the folder "dat"  

Note that the plots may look different than the ones in the paper because the observations are randomly generated  

#------- Figure 1  

python main.py
 
#------- Figure 3  

python main.py --FWERrange "4, 8, 12, 6" --mu-N "0"
python main.py --FWERrange "4, 8, 12, 6" --mu-N "0" --mode 1
python main.py --FWERrange "4, 8, 12, 6" --mu-N "0" --mode 2

#------- Figure 4  

python main.py --FWERrange "3, 4"

#------- Figure 5

python main.py --FWERrange "2, 4" --mu-N "0"
python main.py --FWERrange "2" --mu-N "0, -0.3, -1, -2" --plot-style "4"
      
#------- Figure 6

python main.py --FWERrange "1,2,3,4" --mu-N "-0.5, -1, -1.5" --mu-A "4"  
python main.py --FWERrange "1,2,3,4" --mu-N "0" --mu-A "4, 5"

--------------------------------------------------------------------------------------------------------------------------------------------  

This code borrowed substantial parts from Tijana Zrnic's code available at: https://github.com/tijana-zrnic/SAFFRONcode
If you spot any issues or bugs, please contact me at jinjint(at)andrew(dot)cmu(dot)edu

