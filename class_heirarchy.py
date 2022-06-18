#!/usr/bin/python

import re
import networkx as nx
import os

prog = re.compile(r"class (?P<subclass>\w+)(\((?P<superclasses>[\s\w,=.]*)\))*:")

def grep_stream(location):
    return os.popen(
        r'find %s -name "*.py" | xargs grep -h "^class"'%location)
def nx_from_stream(f):
    #assert isinstance(f, TextIOBase)
    G = nx.DiGraph()
    for line in f:
        match = prog.match(line)
        if not match:
            continue
        subclass = match.groupdict()['subclass']
        if match.groupdict()['superclasses'] is not None:
            for superclass in match.groupdict()['superclasses'].split(','):
                G.add_edge(superclass.strip(), subclass)
        else:
            G.add_node(subclass)
    return G

if __name__ == "__main__":
    from sys import argv, exit
    if len(argv) == 3:
        location, name = argv[1:]
    else:
        print("Usage:\n%s sympy/core/ outfile_file_name"%argv[0])
        exit()
    stream = grep_stream(location)
    G = nx_from_stream(stream)
    Gpd = nx.nx_pydot.to_pydot(G)
    Gpd.set_rankdir("LR")
    Gpd.set_overlap("false")
    Gpd.write("%s.dot"%name)
    os.system("dot -Tpdf %s.dot -o %s.pdf"%(name, name))