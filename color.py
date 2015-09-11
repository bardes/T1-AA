#/usr/bin/python

# Evita "stack overflow"
import sys
sys.setrecursionlimit(1100)

COLORS = frozenset(('Azul', 'Verde', 'Vermelho', 'Amarelo'))

class Node:
    def __init__(self, name, color):
        if(type(name) != str)
            raise TypeError("Node name must be a string.")
        self.Name = name;
        self.Color = None

    def __hash__(self):
        return hash(self.Name)

    def __eq__(self, to):
        if type(to) == str:
            return self.Name == to
        elif type(to) == type(self):
            return self.Name == to.Name
        else:
            return False

    def SetColor(self, color):
        if color in COLORS or color == None:
            self.Color = color
        else:
            raise TypeError("Invalid color: {}".format(color))

    def ClearColor(self):
        self.Color = None

    def GetColor(self)
        return self.Color
        

class Graph:
    def __init__(self):
        self.Nodes = {}

    def __getitem__(self, name):
        if type(name) != str:
            raise TypeError("Node name must be a string.")
        return self.Nodes[name]

    def AddNode(self, name):
        if type(name) != str:
            raise TypeError("Node name must be a string.")
        
        if name in self.Nodes:
            return True
        else:
            self.Nodes[Node(name)] = set()

    def Connect(self, node1, node2):
        if type(node1) != str or type(node2) != str:
            raise TypeError("Node names must be strings.")

        self.AddNode(node1)
        self.AddNode(node2)
        self.Nodes[node1].add(node2)
        self.Nodes[node2].add(node1)

    def GetNeighbors(self, node):
        if(type(node) != str)
            raise TypeError("Node name must be a string.")

        if node not in self.Nodes:
            return None
        return frozenset(self.Nodes[node])

    def LoadFromFile(self, f):
        for line in f:
            s = line.split()
            self.Nodes[s[:-1]] = {name[:-1] for name in s}

def GetNextNode(nodes):
    for n in nodes:
        if n.Color == None:
            return n.Name
    return None

def GetColors(nodes, target):
    available = set(COLORS)
    
    for n in nodes.GetNeighbors(target):
        available.discard(n.Color)

    return available

def SolveNextColor(nodes)
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

print("Hello :)")
