import hashlib
import os
import datetime
import sys

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compareTables(A,B):
    onlyInA = []
    onlyInB = []
    correlation = []

    for k in A.keys():
        if k in B:
            correlation += [(A[k],B[k])]
            del B[k]
        else: onlyInA += [A[k]]

    for k in B.keys():
        onlyInB += [B[k]]

    return (onlyInA, onlyInB, correlation)

def addDirToTable(path, table):
    for root, subdirs, files in os.walk(path):
        for f in files:
            fullPath = os.path.join(root,f)
            md5Val = md5(fullPath)
            table[md5Val] = fullPath




srcPaths = [sys.argv[1]]
srcTable = {}

dstPaths = [sys.argv[2]]
dstTable = {}

for p in srcPaths:
    print "collecting from " + p + " ; " + str(datetime.datetime.now())
    sys.stdout.flush()
    addDirToTable(p, srcTable)

for p in dstPaths:
    print "collecting from " + p + " ; " + str(datetime.datetime.now())
    sys.stdout.flush()
    addDirToTable(p, dstTable)

print "Comparing collections " + str(datetime.datetime.now())
sys.stdout.flush()
onlyInA , onlyInB, correlation = compareTables(srcTable, dstTable)

print "Files only in both sets:"
sys.stdout.flush()
for f in correlation:
    print f

print "Files only in " + str(srcPaths) + " :"
sys.stdout.flush()
for f in onlyInA:
    print f

print "Files only in " + str(dstPaths) + " :"
sys.stdout.flush()
for f in onlyInB:
    print f
