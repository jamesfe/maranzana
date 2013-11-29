import re, os, sys


def loadTable(inFile):
    ''' given a file in the form Letter[space]dist[space]dist...
        where letters start a A and end at some other letter
        in triangular matrix format...creates a graph structure
    '''
    inF = file(inFile, 'r')
    titles = [chr(i) for i in range(65, 78)]
    datTab = dict()
    for t in titles:
        datTab[t] = dict()
    for k in inF:
        k = k.strip()
        curDat = k[0]
        items = k[2:].split(" ")
        for i in range(len(items)):
            offSet = ord(curDat)+i
            datTab[curDat][chr(offSet)] = int(items[i])
    return(datTab)

def getDist(graph, fr, to):
    ''' wrapper class.  checks to/from and returns distance from
        table.  bc the table is a triangular matrix, half the refs
        are invalid so it flips unordered pairs 
    '''
    if(fr>to):
        totemp = to
        to = fr
        fr = totemp
    ## we always want the from to be less than the to
    return(int(graph[fr][to]))

def calcWeights(w):
    ''' given an array of weights, returns a dict indexed by 
        letters for which each has a weight.  starts at A 
    '''
    lets = [chr(i) for i in range(65, 65+len(w))]
    retDict = dict()
    for let in range(len(lets)):
        retDict[lets[let]] = w[let]
    return(retDict)

def assign(graph, node, fac):
    ''' given a graph in the standard form, a node, and a list 
        of facilities, this will identify the facility that is 
        closest to the node and return that letter
    '''
    minDist = float('inf')
    tgtFac = ''
    for f in fac:
        nDist = getDist(graph, node, f)
        #print node, f, nDist
        if(nDist < minDist):
            minDist = nDist
            tgtFac = f
    #print tgtFac
    return(tgtFac)

def printG(graph):
    for k in sorted(graph):
        print k, graph[k]

def pickNewCenter(graph, wgts, fac):
    ''' given a graph in the standard form, facility/weight dict
        and a facility (with list of members), picks a new 
        center for each facility grouping
    ''' 
    minDest = float('inf')
    minFac = ''
    for dest in fac[1]:
        sumDest = 0
        for dest2 in fac[1]:
            sumDest+=(wgts[dest2]* getDist(graph, dest, dest2))
        #print dest, sumDest
        if(sumDest<minDest):
            minDest = sumDest
            minFac = dest
    print "New Center: "+minFac+" ("+str(minDest)+")"
    return(minFac)

def runModel(distG, weightD, nodes, facilities):
    while(True):
        for node in nodes:
            ## each node has a letter and a space for the 
            ## facility it is assigned to
            assn = assign(distG, node[0], facilities)
            node[1] = assn
            #print node[0], "Assign: ", assn
        print "Calculated partitions: "
        for k in facilities:
            print k+": ", ' '.join([i[0] for i in nodes if(i[1]==k)])
        facNodes = [[i, []] for i in facilities]
        #print facNodes
        for fac in facNodes:
            r = [i[0] for i in nodes if(i[1]==fac[0])]
            for t in r:
                fac[1].append(t)
        #print facNodes
        newFacs = []
        for fac in facNodes:
            newFacs.append(pickNewCenter(distG, weightD, fac))
        print "New selections: ",newFacs
        if(sorted(newFacs)==sorted(facilities)):
            break
        facilities = newFacs
    return(facilities)

if(__name__=="__main__"):
    distG = loadTable("./matData.txt")
    #printG(distG)
    weights = [120, 210, 80, 100, 680, 520, 75, 120, 800, 170, 70, 105, 70]
    # These should be changed per the matrix data
    weightD = calcWeights(weights)
    nodes = [[chr(i), ''] for i in range(65, 78)]
    facilities = ['A', 'H']
    #facilities = ['I', 'F']
    resDict = dict()
    for fr1 in nodes:
        for fr2 in nodes:
            if(fr1[0]!=fr2[0]):
                seeds = [fr1[0], fr2[0]]
                print "-----------------------------------------------------"
                print "Running model with seeds: "+' '.join(seeds)
                rs = sorted(runModel(distG, weightD, nodes, seeds))
                if(''.join(rs) in resDict):
                    resDict[''.join(rs)]+=1
                else:
                    resDict[''.join(rs)]=1
    print "Summary of number of times each solution occurred:"
    for k in resDict:
        print k, resDict[k]

    ## Synopsis of the algorithm:
    ## 1. Load distance tables, weight tables, etc.
    ## 2. Begin permutations: 
    ## 2a. Seed Facilities (array)
    ## 2b. Assign nodes to seeds
    ## 2c. Calculate new facilties to replace seeds
    ## 3. Repeat 2 until nothing changes
