from instructions import *
from program import *
from saveload import *

class Simulation:

    def __init__(self, memsize=9080, ft = 20, copy=.001):
        self.memory = [-1 for i in range(memsize)]
        self.phylo = {}
        self.reaper_queue = []
        self.organisms = []
        self.fail_threshold = ft
        self.copy_error_rate = copy

    def seed(self, ancestor = 'ancestor.txt'):
        src = open(ancestor, 'r')
        genes = []
        for line in src.readlines():
            genes = genes + line.strip().split() if line[0] != '\\' else genes
        for i in range(9000,9000+len(genes)):
            self.memory[i] = int(genes[i-9000],16)
        src.close()
        Program(self,(9000,len(genes)))

    def clearmemory(self,ind):
        self.memory[ind.loc: ind.loc + ind.size] = [-1 for i in range(ind.loc, ind.loc + ind.size)]
        
    def add_phylo(self,ind):
        if ind.id not in self.phylo: self.phylo[ind.id] = ind.parent

    def add_ind(self,ind):
        self.reaper_queue.insert(0, ind)
        self.add_phylo(ind)
        self.organisms.append(ind)
        saveOrganism(ind,self.phylo)

    def run(self): 
        i = 0
        while i < 95000:
            for c in self.organisms:
                ind = c
                # print ind.ip, '|', ind.ax, ind.bx, ind.cx, ind.dx, 'Err:', ind.fail, ind.offspring, '\t\t|', hex(self.memory[ind.ip]), instructions[self.memory[ind.ip]].__name__
                instructions[self.memory[ind.ip]](ind)
                ind.ip = wrapcheck(self.memory,ind.ip)
                i += 1 
                if ind.fail >= self.fail_threshold: 
                    self.organisms.remove(ind)
                    self.reaper_queue.remove(ind)
                    self.clearmemory(ind)
            if not self.organisms: self.seed()

