from abc import abstractmethod
from main.experiments.ClusterTools import ClusterTools
from main.experiments.Experiment import Experiment
from main.tools.GitTools import GitTools
from pickle import load
from sets import Set
import os

class ExperimentAggregator(object):
    def __init__(self, folders):
        assert(len(folders) > 0)
        self.folders = folders
        
        # load first git version
        assert(os.path.exists(folders[0]))
        f = open(folders[0] + Experiment.gitversion_filename)
        ref_githash = f.readline().strip()
        ref_gitbranch = f.readline().strip()
        f.close()
        
        to_ignore = Set()
        
        # compare to all others
        for i in range(len(folders)):
            # assert that all experiments ran under the same git version
            if not os.path.exists(folders[i]):
                print "folder", folders[i], "does not exist, ignoring"
                to_ignore.add(i)
                continue
            
            f = open(folders[i] + Experiment.gitversion_filename)
            githash = f.readline().strip()
            gitbranch = f.readline().strip()
            f.close()
            
            # assert that all git hashs are equal
            assert(githash == ref_githash)
            assert(gitbranch == ref_gitbranch)
            
            # this might be false if script was altered after experiment, comment out then
            if githash != GitTools.get_hash():
                print "git version in folder", folders[i], "is", githash, "while " \
                      "git version in folder", folders[0], "is", ref_githash
                 
            if gitbranch != GitTools.get_branch():
                print "git branch in folder", folders[i], "is", gitbranch, "while " \
                      "git branch in folder", folders[0], "is", ref_gitbranch
                      
        # remove non-existing folders
        folders_cleaned=[]
        for i in range(len(folders)):
            if i not in to_ignore:
                folders_cleaned.append(folders[i])
            
        self.folders=folders_cleaned
    
    def load_raw_results(self):
        self.experiments = []
        for i in range(len(self.folders)):
            filename = self.folders[i] + Experiment.experiment_output_folder + \
                     os.sep + Experiment.erperiment_output_filename
            
            try:
                f = open(filename , "r")
                self.experiments.append(load(f))
                f.close()
            except IOError:
                print "skipping", filename, "due to IOError"
                errorfilename=self.folders[i] + ClusterTools.cluster_error_filename
                try:
                    ef = open(errorfilename)
                    lines=ef.readlines()
                    print "cluster error output"
                    print lines + "\n\n"
                except IOError:
                    print "could not find cluster error file", errorfilename, "due to IOError"
        
        print "loaded", len(self.experiments), "experiments"
                
    def aggregate(self):
        self.load_raw_results()
        self.__process_results__()
    
    @abstractmethod
    def __process_results__(self):
        raise NotImplementedError()