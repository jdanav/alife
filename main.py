from simulation import Simulation
from phylo import *

x = Simulation()
x.seed()
x.run()
print 'id\t\t| ax\tbx\tcx\tdx\tfail\tip\tsize\tloc'
for i in x.organisms: print '%s\t| %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (i.id[::3],i.ax, i.bx, i.cx, i.dx, i.fail, i.ip, i.size, i.loc)
