def phy_descend(parent, dictionary, out={}):
    if parent not in out:
        out[parent] = {}
        for i in dictionary.keys():
            if dictionary[i] == parent: phy_descend(i, dictionary, out[parent])
    return out

def phy_ancestry(child, dictionary, out=[]):
    if child in dictionary.keys():
        out.append(child)
        phy_ancestry(dictionary[child], dictionary, out)
    return out

def phy_stratus(dictio, layer=0):
    if layer == 0: stratus = dictio.keys()
    else:
        stratus = []
        for i in dictio.keys():
            stratus = stratus + phy_stratus(dictio[i], layer - 1)
    return stratus
clean = []

def phy_toclean(family, indent=0, preceding='', printed=[]):
    if None in family.keys(): family = family[None]
    print("|")
    if len(family) > 1: preceding += '|'
    else: preceding += ''

    for parent in family:
        clean.append(preceding + '|__' + parent)
        phy_toclean(family[parent], indent + 1, preceding + '   ', printed + [parent])

def cleanlines(clean=[]):
    clean = clean[::-1]
    for n in range(0,len(clean)):
        newline = ''
        for i in range(len(clean[n])):
            tc = clean[n][i]
            if clean[n][i:i+2] == '||': tc = ''
            if clean[n][i:i+2] == '| ' and \
            (len(clean[n-1]) < i or \
            (len(clean[n-1]) > i and clean[n-1][i] == ' ')): tc = ' '
            else: newline = newline + tc
        clean[n] = newline
    for i in clean[::-1]: print i
