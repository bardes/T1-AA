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
        self.AvailableColors = set(COLORS)

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
        return self.Nodes[name][0]

    def __str__(self):
        return str(self.Nodes)

    def __iter__(self):
        for node in self.Nodes.values():
            yield node[0]
        raise StopIteration

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
        elif (self[node1].Color == self[node2].Color) and self[node1].Color:
            raise Exception("Cannot connect nodes of the same color!")

        self.AddNode(node1)
        self.AddNode(node2)
        self.Nodes[node1][1].add(node2)
        self.Nodes[node2][1].add(node1)
        self.CalcAvailableColors(node1)
        self.CalcAvailableColors(node2)

    def GetNeighbors(self, name):
        if not isinstance(name, str):
            raise TypeError("Node name must be a string.")

        if name not in self.Nodes:
            return None
        return frozenset(self.Nodes[name][1])

    def Paint(self, target, color):
        if color not in COLORS:
            raise TypeError("Invalid color: \"{}\"".format(color))
        elif color not in self[target].AvailableColors:
            return False

        if(self[target].Color != None):
            self.Unpaint(target)

        self[target].SetColor(color)
        for node in self.GetNeighbors(target):
            self[node].AvailableColors.discard(color)

        return True

    def CalcAvailableColors(self, target):
        self[target].AvailableColors = set(COLORS)
        for n in self.GetNeighbors(target):
            self[target].AvailableColors.discard(self[n].Color)

    def Unpaint(self, target):
        self[target].Color = None
        for n in self.GetNeighbors(target):
            self.CalcAvailableColors(n)

    def LoadFromFile(self, f):
        for line in f:
            s = line[:-1].split(':')
            self.Nodes[s[0]] = (Node(s[0]), set(s[1].split(',')))

    def ValidadteSymmetry(self):
        flag = True
        for node in self.Nodes:
            for neighbor in self.GetNeighbors(node):
                if neighbor not in self.Nodes:
                    print("Warning: non existent node \"{}\"" \
                            .format(neighbor), file=sys.stderr)
                    flag = False
                elif node not in self.GetNeighbors(neighbor):
                    print("Warning: non symmetric edge from {} to {}" \
                            .format(node, neighbor), file=sys.stderr)
                    flag = False
        return flag

def GetNextNode(nodes):
    for n in nodes:
        if n.Color == None:
            return n
    return None

def GetColors(nodes, target):
    return frozenset(nodes[target].AvailableColors)

def SolveNextColor(nodes):
    # Determina o próximo nó a ser aprofundado
    target = GetNextNode(nodes)

    # Se não tem mais nós achou a solução.
    if target == None:
        return True;

    # Pra cada possível solução
    for color in COLORS:
        if nodes.Paint(target.Name, color): # Tenta pintar o nó
            if not SolveNextColor(nodes):   # Tenta aprofundar ainda mais
                nodes.Unpaint(target.Name)  # Se não conseguiu desfaz a pintura
            else:
                return True # Se achou uma solução retorna True

    # Se nenhuma cor levou a uma solução, falha.
    return False

if __name__ == '__main__':
    nodes = Graph() # Cria um grafo vazio

    # Tenta abrir o arquivo dado e pular a primeira linha
    infile = open(sys.argv[1])
    infile.readline()

    # Carrega os dados e fecha o arquivo
    nodes.LoadFromFile(infile)
    infile.close()

    # verifica se grafo lido é válido
    if(nodes.ValidadteSymmetry() == False):
        sys.exit(1) # Se não for sai com erro

    # Começa o backtracking
    SolveNextColor(nodes)

    # Imprime os resultados
    for n in nodes:
        print("{}: {}".format(n.Name, n.Color))
