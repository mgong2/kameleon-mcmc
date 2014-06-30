"""
Copyright (c) 2013-2014 Heiko Strathmann, Dino Sejdinovic
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 *
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 *
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the author.
"""
from kameleon_mcmc.tools.GenericTests import GenericTests
import numpy as np


class ConvergenceStats():
    '''
    Class that implements various convergence statistics for Markov chains
    '''

    @staticmethod
    def autocorr(x):
        """
        Computes the (optionally: normalised) auto-correlation function of a
        one dimensional sequence of numbers.
        
        Utilises the numpy correlate function that is based on an efficient
        convolution implementation.
        
        Inputs:
        x - one dimensional numpy array
        
        Outputs:
        Vector of autocorrelation values for a lag from zero to max possible
        """
        
        GenericTests.check_type(x, "x", np.ndarray, 1)
        
        # normalise, compute norm
        xunbiased = x - np.mean(x)
        xnorm = np.sum(xunbiased ** 2)
        
        # convolve with itself
        acor = np.correlate(xunbiased, xunbiased, mode='same')
        
        # use only second half, normalise
        acor = acor[len(acor) / 2:] / xnorm
        
        return acor
        