import sys, re, json

def _progBar(count, max_count, l=30, u=100):
    if count%u != 0:
        return
    prog = 1+int(l*(count/float(max_count)))
    if count is 0:
        prog = 0
    prog_left = l - prog
    sys.stdout.write("|" + u"\u2588"*prog + u"\u2591"*prog_left + "|\r")
    sys.stdout.flush()

def _chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def loadFile(filePath):
    out = []
    with open(filePath, "r") as file:
        for line in file:
            out.append(line)
    return out

def loadJSON(filePath):
    out = ""
    with open(filePath, "r") as file:
        for line in file:
            out += line
    return json.loads(out)

def saveFile(filePath, out):
    with open(filePath, "w") as file:
        for line in out:
            file.write(''.join(json.dumps(line).split()) + '\n')

def saveJSON(filePath, out):
    with open(filePath, "w") as file:
        file.write(''.join(json.dumps(out).split()) + '\n')
