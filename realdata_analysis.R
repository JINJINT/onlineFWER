#============ loading packages ==============#

library(ggplot2)
library(reshape2)
library(tikzDevice)
library(dplyr)
library(tibble)
library('latex2exp')
library(VGAM)
library(RColorBrewer)
library(onlineFDR)



#============ loading data ==============#

IMPC.data.full = read.csv("./IMPC_ProcessedData_Continuous.csv")
IMPC.data.full = as_tibble(IMPC.data.full)
IMPC.data = select(IMPC.data.full, Experimental.Id, Latest.Mutant.Assay.Date,
                   Genotype.Contribution, Sd.Contribution)
IMPC.data = arrange(IMPC.data, Experimental.Id, Latest.Mutant.Assay.Date) # order by batch and then time
genotype.pval = pull(select(IMPC.data, Genotype.Contribution))
pvec = genotype.pval

# transfer the batch infomation into lags
batches = as.vector(table(IMPC.data.full$Experimental.Id)) 
lags = c()
batch_index = c()
for(k in 1:length(batches)){
  lags = c(lags, 0:(batches[k]-1))
  batch_index = c(batch_index, rep(k, batches[k]))
}

# form the final dataset
pvecdata = data.frame(batch =  batch_index, value = -log10(pvec))
pvecdata = pvecdata[which(pvecdata$value!=Inf), ] # remove the corrupted data
mdata = melt(pvecdata, id.vars = "batch", measure.vars = "value")

# visualize the batch strucuture of the data using subsamples
colors = brewer.pal(n = 7, name = "RdYlBu")
mdat = mdata[1:5000,]
ggplot(mdat, aes(x = 1:length(value), y = value, color = as.factor(bat))) +
  geom_bar(stat="identity", alpha = 0.8) +
  scale_color_manual(values = rep(c("grey", "skyblue"), 1449)) +
  scale_y_continuous(expand = c(0, 0) ) +  
  labs(x = "time", y = TeX("$-log_{10}(P)$"))+
  theme_bw() +
  theme( 
    legend.position="none",
    panel.border = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.minor.x = element_blank()
  )



#============ testing ==============#

# compute the underlying gamma sequence
gamma = 1/c(1:(length(pvec)))^{1.1}
gamma = gamma/zeta(1.1)

alpha_list = c(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4)
discovery_mat = matrix(0, length(alpha_list), 3)
colnames(discovery_mat) = c("Alpha-Spending", "Online-Fallback", "Adaptive-Spending", "Discard-Spending", "ADDIS-Spending")
rownames(discovery_mat) = alpha_list

for(i in 1:length(alpha_list)){
  # Alpha-Spending
  AS = Alpha_spending(pvec, alpha = alpha_list[i], gammai = gamma)
  R.AS = AS$R
  
  # Online-Fallback
  OF = online_fallback(pvec, alpha =  alpha_list[i], gammai = gamma)
  R.OF = OF$R

  # ADDIS-Spending
  AD = ADDIS_spending(pvec, alpha =  alpha_list[i], gammai = gamma, dep = TRUE, lags = lags)
  R.AD = AD$R

  discovery_mat[i,] = c(sum(R.AS), sum(R.OF), sum(R.AD))
  print(discovery_mat[i,])
}

# plot the results
names <- c("Alpha-Spending", "Online-Fallback", "ADDIS-Spending")
colors<- c("royalblue", "firebrick", "forestgreen")
data = melt(discovery_mat)
data$alpha = alpha_list
ggplot(data = data, aes(x = Var1, y = value, color = as.factor(Var2))) + 
  geom_line() +
  geom_point() +
  scale_shape_manual(values=c(19, 3)) +
  labs(x ="FWER level", y = "Number of discoveris", color = "Methods", title = "") +
  scale_color_manual(values = colors) +
  theme_bw() +
  theme(axis.text.y = element_text(size=8),
        axis.text.x = element_text(size=8),
        axis.title.x = element_text(size=13),
        axis.title.y = element_text(size=13),
        plot.title=element_text(hjust=0,size=18)
  )

