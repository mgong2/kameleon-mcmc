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
from abc import abstractmethod
from numpy import ones, mod, arange
import numpy
from numpy.random import permutation, randint

from kameleon_mcmc.distribution.Distribution import Distribution


class FullConditionals(Distribution):
    """
    Base class for Targets in Gibbs sampling. This implements a number of
    schedules how Gibbs will iterate over the variables. This class is to be
    put together with an MH algorithm, i.e. it will generate samples from the
    full conditionals (given a schedule) and always return 1 as the log_pdf
    (leading to unconditional acceptance of any sample).
    
    Possible schedules are:
    in_turns           - Iterates a particular order (given by constructor)
    random_permutation - Iterates randomly, but without repetition per block
    random_repetition  - Iterates completely random, with repetitions per block
    """
    schedules = ["in_turns", "random_permutation", "random_repetition"]
    
    def __init__(self, current_state, schedule, index_block=None):
        """
        current_state - Current point of the Gibbs sampler
        schedule      - Schedule for variables
        index_block   - If schedule is "in_turns", this can specify the order.
                        If not specified, arange(dimension) is used
        """
        if not type(current_state) is numpy.ndarray:
            raise TypeError("Current state must by numpy array")
        
        if not len(current_state.shape) is 1:
            raise ValueError("Current state must by 1D numpy array")
        
        Distribution.__init__(self, len(current_state))
        
        if index_block is None:
            index_block = arange(self.dimension)
        
        if not type(schedule) is type(""):
            raise TypeError("Schedule must be a string") 
        
        if not schedule in FullConditionals.schedules:
            raise ValueError("Unknown schedule") 
        
        if not type(index_block) is numpy.ndarray:
            raise TypeError("Index block must by numpy array")
        
        if not len(index_block.shape) is 1:
            raise ValueError("Index block must by 1D numpy array")
        
        if not index_block.dtype is numpy.int:
            raise ValueError("Index block must by int numpy array")
        
        if not len(index_block) is self.dimension:
            raise ValueError("Index block must be of same dimension as distribution")
        
        self.current_state = current_state
        self.schedule = schedule
        self.index_block = index_block
        
        # initialise with last, to cause the first sample come from the first
        self.current_idx = self.dimension
    
    def __str__(self):
        s = self.__class__.__name__ + "=["
        s += "current_state=" + str(self.current_state)
        s += ", schedule=" + str(self.schedule)
        s += ", index_block=" + str(self.index_block)
        s += ", current_idx=" + str(self.current_idx)
        s += ", " + Distribution.__str__(self)
        s += "]"
        return s
    
    def sample(self, n=1):
        if n is not 1:
            raise ValueError("Only one sample supported for full conditionals")
        
        # random schedules need to re-create index block upon last index
        if self.current_idx == self.dimension:
            if self.schedule == "random_permutation":
                self.index_block = permutation(self.index_block)
            elif self.schedule == "random_repetition":
                self.index_block = randint(0, self.dimension, self.dimension)
            
        # update current index
        self.current_idx = mod(self.current_idx + 1, self.dimension)
        idx = self.index_block[self.current_idx]

        # update current state at scheduled index and return a copy
        self.current_state[idx] = self.sample_conditional(idx)
        
        return self.current_state.copy()
    
    def log_pdf(self, X):
        """
        For embedding this in the MH sampler, we always return 1 here to accept
        all samples.
        """
        return ones(len(X))
    
    @abstractmethod
    def sample_conditional(self, index):
        """
        The concrete full conditional distributions (and sampling from them)
        is implemented in sub-classes.
        
        index - Index to sample the full conditional of given all the others
        """
        if index < 0 or index >= self.dimension:
            raise ValueError("Conditional index out of bounds")
        
        raise NotImplementedError()
    