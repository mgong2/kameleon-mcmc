"""
Copyright (c) 2013-2014 Heiko Strathmann
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
from numpy import log, zeros, sqrt
from numpy.random import randn
from scipy.special import betaln
from scipy.io import savemat



class HelperFunctions():
    @staticmethod
    def log_bin_coeff(n, k):
        """
        Compute log binom_coeff(n, k), i.e. the log of the number of possibilities
        to draw k from n
        """
        return -betaln(1 + n - k, 1 + k) - log(n + 1)
    
    @staticmethod
    def generateOU(n=50,alpha=0.95):
        """
        Generate a draw from the Ornstein-Uhlenbeck process
        """
        w=zeros(n)
        w[0]=randn(1)
        for i in range(n-1):
            w[i+1]=alpha*w[i]+sqrt(1-alpha**2)*randn(1)
        return w
    
    @staticmethod
    def export_to_matlab(samples, location):
        savemat(location,mdict={'samples': samples})
        return None