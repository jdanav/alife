from hashlib import md5

class Program:

    def __init__(self, sim, dimensions, parent = None):
        self.sim = sim
        self.parent = parent
        self.loc = dimensions[0]
        self.size = dimensions[1]
        self.genome = [hex(sim.memory[i]) for i in range(self.loc, self.loc + self.size)]
        
        self.id = self.id()

        self.ax = 0; self.bx = 0
        self.cx = 0; self.dx = 0
        self.ip = self.loc

        self.stack = []
        self.fail = 0
        self.offspring = False
        sim.add_ind(self)
        
    def id(self):
        return md5(' '.join(str(self.genome))).hexdigest()

    def __str__(self):
        return self.id
