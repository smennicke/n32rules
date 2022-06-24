#!/usr/bin/python3

import sys
import os

prefixes = {
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    '': 'http://www.example.org/'
}

def prettyPrintPrefixes():
    for s, l in prefixes.items():
        print(f"@prefix {s}: <{l}>.")
    print()

def addPrefix(s : str, l : str):
    prefixes[s] = l

def unfoldOrNothing(s : str):
    if s.count(":"):
        pre, post = s.split(":")
        return f"<{prefixes.get(pre)}{post}>"
    return s

def defaultns(s : str):
    return f":{s}"

def foldOrDefault(s : str):
    if s.startswith('"'):
        return s
    for ns, val in prefixes.items():
        if s.count(val):
            return f"<{ns}:{s.rfind(val)+len(val)}>"
    return defaultns(s)

def unary(p : str, s : str):
    return f"{s} a {p}"

def binary(p : str, s : str, o : str):

    return f"{s} {p} {o}"

bodyv = []

def variableOrConstant(s : str, abv = False):
    # print(f"variableOrConstant: {s}")
    if s.startswith("?"):
        if (abv):
            bodyv.append(s)
            return s
        else:
            if s in bodyv:
                return s
            else:
                return s.replace("?","_:")
    return foldOrDefault(s)

def triplify(s : str, abv = False):
    # print(f"triplify: {s}")
    p, r = s.split("(")
    if r.count(","):
        s, o = r.split(",")
        # print(f"{s} split {p} split {o}")
        return binary(variableOrConstant(p.strip(), abv), variableOrConstant(s.strip(), abv), variableOrConstant(o.strip(), abv))
    else:
        return unary(variableOrConstant(p.strip(), abv), variableOrConstant(r.strip(), abv))

prettyPrintPrefixes()

for fn in sys.argv[1:]:
    p = os.path.basename(fn)
    p = p[:p.rindex(".")]
    with open(fn) as f:
        for line in f:
            if (line.count(",")): # binary case
                s, o = line.split(",")
                print(f"{foldOrDefault(s.strip())} {foldOrDefault(p.strip())} {foldOrDefault(o.strip())}.")
            else:
                print(f"{foldOrDefault(line.strip())} a {foldOrDefault(p.strip())}.")
