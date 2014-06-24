# SAVE FUNCTIONS

def savePhylo(phylo):
    pass

def saveOrganism(ind,phylo):
    output = open(ind.id+'.txt','w')
    output.write('''\\\ ARTIFICIAL LIFE SIMULATOR
\\\ SIZE: %s
\\\ ID: %s
\\\ PARENT: %s
\\\ LOCATION: %s
\\\ GENOME:
%s''' % (ind.size,ind.id, phylo[ind.id], ind.loc, ' '.join(ind.genome)))
    output.close()

# LOAD FUNCTIONS
