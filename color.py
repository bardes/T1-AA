#!/usr/bin/python3

# Evita "stack overflow"
import sys
sys.setrecursionlimit(1100)

COLORS = frozenset({'Azul', 'Verde', 'Vermelho', 'Amarelo'})

class Node:
    def __init__(self, name, color=None):
        if not isinstance(name, str):
            raise TypeError("Node name must be a string.")
        self.Name = name;
        self.Color = color

    def __hash__(self):
        return hash((self.Name, "NODE"))

    def __eq__(self, to):
        if isinstance(to, self.__class__):
            return self.Name == to.Name
        elif isinstance(to, str):
            return self.Name == to
        else:
            return False

    def __str__(self):
        return "<Node: {}, {}>".format(self.Name, self.Color or "[em branco]")

    def SetColor(self, color):
        if color in COLORS or color == None:
            self.Color = color
        else:
            raise TypeError("Invalid color: {}".format(color))

    def ClearColor(self):
        self.Color = None

    def GetColor(self):
        return self.Color


class Graph:
    def __init__(self):
        self.Nodes = {}

    def __getitem__(self, name):
        if not isinstance(name, str):
            raise TypeError("Node name must be a string.")
        return self.Nodes[name][0]

    def __str__(self):
        return str(self.Nodes)

    def AddNode(self, name):
        if not isinstance(name, str):
            raise TypeError("Node name must be a string.")

        if name in self.Nodes:
            return True
        else:
            self.Nodes[name] = (name, set())

    def Connect(self, node1, node2):
        if not isinstance(node1, str) or not isinstance(node2, str):
            raise TypeError("Node names must be strings.")
        self.AddNode(node1)
        self.AddNode(node2)
        self.Nodes[node1][1].add(node2)
        self.Nodes[node2][1].add(node1)

    def GetNeighbors(self, name):
        if not isinstance(name, str):
            raise TypeError("Node name must be a string.")

        if name not in self.Nodes:
            return None
        return frozenset(self.Nodes[name][1])

    def LoadFromFile(self, f):
        for line in f:
            s = line.split()
            node_name = s[0][:-1]
            self.Nodes[node_name] = (Node(node_name),
                                     set([name[:-1] for name in s[1:]]))

def GetNextNode(nodes):
    for n in nodes.Nodes:
        if nodes[n].Color == None:
            return n
    return None

def GetColors(nodes, target):
    available = set(COLORS)

    for n in nodes.GetNeighbors(target):
        available.discard(nodes[n].Color)

    return available

def SolveNextColor(nodes):
    # Determina o próximo nó a ser aprofundado
    target = GetNextNode(nodes)

    # Se não tem mais nós achou a solução.
    if target == None:
        return nodes;

    # Pra cada possível solução
    for color in GetColors(nodes, target):
        nodes[target].SetColor(color) # Atribui a cor
        nodes = SolveNextColor(nodes) # Tenta aprofundar ainda mais

        if not nodes:
            # Se não conseguiu aprofundar troca de cor
            nodes[target].ClearColor()
        else:
            # Se achou uma solução retorna
            return nodes

    # Se nenhuma cor levou a uma solução, falha.
    return None

nodes = Graph()
f = open('in')
_type = f.readline().split()[1]
nodes.LoadFromFile(f)
f.close()

SolveNextColor(nodes)

for n in nodes.Nodes:
    print("{}: {}".format(nodes[n].Name, nodes[n].Color))