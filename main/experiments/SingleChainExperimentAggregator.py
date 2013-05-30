from main.experiments.ExperimentAggregator import ExperimentAggregator
from matplotlib.pyplot import plot, show, fill_between, savefig
from numpy.linalg.linalg import norm
from numpy.ma.core import arange, zeros, mean, std, allclose, cumsum, array, \
    sqrt

class SingleChainExperimentAggregator(ExperimentAggregator):
    def __init__(self, folders, ref_quantiles=arange(0.1, 1, 0.1)):
        ExperimentAggregator.__init__(self, folders)
        self.ref_quantiles = ref_quantiles
    
    def __process_results__(self):
        lines = []
        if len(self.experiments) == 0:
            lines.append("no experiments to process")
            return
        
        # burnin is the same for all chains
        burnin = self.experiments[0].mcmc_chain.mcmc_params.burnin
        
        quantiles = zeros((len(self.experiments), len(self.ref_quantiles)))
        norm_of_means = zeros(len(self.experiments))
        acceptance_rates = zeros(len(self.experiments))
        
        for i in range(len(self.experiments)):
            burned_in = self.experiments[i].mcmc_chain.samples[burnin:, :]
            
            # use precomputed quantiles if they match with the provided ones
            if hasattr(self.experiments[i], "ref_quantiles") and \
               allclose(self.ref_quantiles, self.experiments[i].ref_quantiles):
                quantiles[i, :] = self.experiments[i].quantiles
            else:
                quantiles[i, :] = self.experiments[i].mcmc_chain.mcmc_sampler.distribution.emp_quantiles(\
                                  burned_in, self.ref_quantiles)
                
            norm_of_means[i] = norm(mean(burned_in, 0))
            acceptance_rates[i] = mean(self.experiments[i].mcmc_chain.accepteds[burnin:])

        mean_quantiles = mean(quantiles, 0)
        std_quantiles = std(quantiles, 0)
        
        lines.append("quantiles:")
        for i in range(len(self.ref_quantiles)):
            lines.append(str(mean_quantiles[i]) + " +- " + str(std_quantiles[i]))
        
        lines.append("norm of means:")
        lines.append(str(mean(norm_of_means)) + " +- " + str(std(norm_of_means)))
        
        lines.append("acceptance rate:")
        lines.append(str(mean(acceptance_rates)))
        
        # add latex table line
        latex_lines=[]
        latex_lines.append("& STM & ADM & ADML & KAM\\\\")
        
        # add latex table line
        latex_lines=[]
        latex_lines.append("Sampler & Acceptance & Norm(mean) & ")
        for i in range(len(self.ref_quantiles)):
            latex_lines.append('%.1f' % self.ref_quantiles[i] + "-quantile")
            if i<len(self.ref_quantiles)-1:
                latex_lines.append(" & ")
        latex_lines.append("\\\\")
        lines.append("".join(latex_lines))
        
        latex_lines=[]
        latex_lines.append(self.experiments[0].mcmc_chain.mcmc_sampler.__class__.__name__)
        latex_lines.append(" & ")
        latex_lines.append('$%.3f' % mean(acceptance_rates) + " \pm " + '%.3f$' % std(acceptance_rates))
        latex_lines.append(" & ")
        latex_lines.append('$%.3f' % mean(norm_of_means) + " \pm " + '%.3f$' % std(norm_of_means))
        latex_lines.append(" & ")
        for i in range(len(self.ref_quantiles)):
            latex_lines.append('$%.3f' % mean_quantiles[i] + " \pm " + '%.3f$' % std_quantiles[i])
            if i<len(self.ref_quantiles)-1:
                latex_lines.append(" & ")
        
        latex_lines.append("\\\\")
        lines.append("".join(latex_lines))
        
        # mean as a function of iterations
        iterations=(arange(len(norm_of_means))+1)
        running_means=cumsum(norm_of_means)/iterations
        running_errors=1.96*array([std(norm_of_means[0:(i+1)]) / sqrt(i+1) for i in range(len(norm_of_means))])
        plot(iterations, running_means)
        fill_between(iterations, running_means-running_errors, \
                     running_means+running_errors, hold=True, color="gray")
        savefig(self.experiments[i].folder_base + "running_mean.png")
        
        return lines

    def __str__(self):
        s = self.__class__.__name__ + "=["
        s += "ref_quantiles=" + str(self.ref_quantiles)
        s += ", " + ExperimentAggregator.__str__(self)
        s += "]"
        return s
