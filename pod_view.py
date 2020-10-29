#!/usr/bin/env python3
import sys

namespaceMap = {}

hostname = ""
def getPodSpec ( token ):
    parts = token.split("\"")
    name = parts[1]
    nameParts = name.split("_")
    podname = nameParts[0] 
    podname = podname.ljust(40, ' ')
    namespace = nameParts[1]
    namespace = namespace.split("(")[0]    
    namespace = namespace.ljust(30, ' ')
    theNamespace = {}
    if namespace not in namespaceMap:
        namespaceMap[namespace] = theNamespace
    else:
        theNamespace = namespaceMap[namespace]

    podStatus = { }

    podStatus["live"] = "----"
    podStatus["ready"] = "----"
    podStatus["livecount"] = 0
    podStatus["readycount"] = 0
    podStatus["node"] = hostname
    if podname not in theNamespace:
        theNamespace[podname] = podStatus
    else:
        podStatus = theNamespace[podname]
    return podStatus

def checkLiveness( token ):
    podSpec = getPodSpec(token)
    if token.endswith("succeeded"):
        if podSpec["live"] == False:
            podSpec["livecount"] = podSpec["livecount"] + 1
        podSpec["live"]=True
    else:
        podSpec["live"]=False

def checkReadiness( token ):
    podSpec = getPodSpec(token)
    if token.endswith("succeeded"):
        if podSpec["ready"] == False:
            podSpec["readycount"] = podSpec["readycount"] + 1
        podSpec["ready"]=True
    else:
        podSpec["ready"]=False

if len(sys.argv) < 2:
    print("A journal must be specified:\npod_view.py /path/to/journal")
    sys.exit(0)

sys.argv.pop(0)

for filename in sys.argv:
    hostname = ""
    with open(filename, "r") as file:
        print("Processing: " + filename)
        for line in file:
            if hostname == "" and line.startswith("--") == False:                
                hostname = line.split(" ")[3]
                print(hostname)
            tokens = line.split("]")
            if len(tokens) >= 3:
                token = tokens[2].strip()
                if token.startswith("Liveness probe"):
                    checkLiveness(token)
                elif token.startswith("Readiness probe"):
                    checkReadiness(token)

print("Namespace".ljust(30, " ")+"\t"+"Pod Name".ljust(40, " ")+"\tIs Alive".ljust(10, " ")+"\tIs Ready".ljust(10, " ")+"\tNode")
for nsname in namespaceMap:        
    for podname in namespaceMap[nsname]:
        podStatus = namespaceMap[nsname][podname]
        print(nsname+"\t"+
            podname+"\t"+
            (str(podStatus["live"])+
            "("+str(podStatus["livecount"])+")").ljust(10, ' ')+"\t"+
            (str(podStatus["ready"]) +
            "("+str(podStatus["readycount"])+")").ljust(10, ' ')+"\t" + 
            podStatus["node"])