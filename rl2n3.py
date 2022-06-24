#!/usr/bin/python3

import sys

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
    elif s.startswith('"'):
        return s
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

with open(sys.argv[1]) as f:
    for line in f:
        if (line.count("->")):
            body, head = line.split("->")
            body = body[:body.rindex(")")]
            head = head[:head.rindex(")")]
            bodys = '. '.join(triplify(t, abv=True) for t in body.split('),'))
            heads = '. '.join(triplify(t) for t in head.split('),'))
            print(f'{{{bodys}}} => {{{heads}}}.')
            bodyv = []
#         if line.lower().count("prefix"):
#             p, s, l = line.split(" ")
#             addPrefix(s[:s.index(":")], l[1:l.index(">")])
#         elif line.count("=>") == 1:
#             body, head = line.split("=>")
#             body = body[body.index("{")+1:body.rindex("}")]
#             head = head[head.index("{")+1:head.rindex("}")]

#             heads = ','.join(f'TI({variableOrConstant(t.split(" ")[0])},{variableOrConstant(t.split(" ")[1])},{variableOrConstant(t.split(" ")[2])})' for t in head.split("."))
#             bodys = ','.join(f'TI({variableOrConstant(t.split(" ")[0])},{variableOrConstant(t.split(" ")[1])},{variableOrConstant(t.split(" ")[2])})' for t in body.split("."))

#             print(f"{heads} :- {bodys}")
#         elif line.count(" ") == 2:
#             s, p, o = line.split(" ")
#             o = o[:o.rindex(".")]
#             print(f"{unfoldOrNothing(s.strip())},{unfoldOrNothing(p.strip())},{unfoldOrNothing(o.strip())}")
#             # print(f"TE({unfoldOrNothing(s.strip())},{unfoldOrNothing(p.strip())},{unfoldOrNothing(o.strip())})")
