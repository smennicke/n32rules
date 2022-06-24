#!/usr/bin/python3

import sys

prefixes = {
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    '': 'http://www.example.org/'
}

def addPrefix(s : str, l : str):
    prefixes[s] = l

def unfoldOrNothing(s : str):
    if s.count(":"):
        pre, post = s.split(":")
        return f"<{prefixes.get(pre)}{post}>"
    return s

def variableOrConstant(s : str):
    if s.startswith("?"):
        return s[1:]
    if s.startswith("_:"):
        return s[2:]
    return unfoldOrNothing(s)

with open(sys.argv[1]) as f:
    for line in f:
        if line.lower().count("prefix"):
            p, s, l = line.split(" ")
            addPrefix(s[:s.index(":")], l[1:l.index(">")])
        elif line.count("=>") == 1:
            body, head = line.split("=>")
            body = body[body.index("{")+1:body.rindex("}")]
            head = head[head.index("{")+1:head.rindex("}")]

            heads = ','.join(f'TI({variableOrConstant(t.strip().split(" ")[0])},{variableOrConstant(t.strip().split(" ")[1])},{variableOrConstant(t.strip().split(" ")[2])})' for t in head.split("."))
            bodys = ','.join(f'TI({variableOrConstant(t.strip().split(" ")[0])},{variableOrConstant(t.strip().split(" ")[1])},{variableOrConstant(t.strip().split(" ")[2])})' for t in body.split("."))

            print(f"{heads} :- {bodys}")
        elif line.count(" ") == 2:
            s, p, o = line.split(" ")
            o = o[:o.rindex(".")]
            print(f"{unfoldOrNothing(s.strip())},{unfoldOrNothing(p.strip())},{unfoldOrNothing(o.strip())}")
            # print(f"TE({unfoldOrNothing(s.strip())},{unfoldOrNothing(p.strip())},{unfoldOrNothing(o.strip())})")
