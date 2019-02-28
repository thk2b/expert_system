import node

class Graph:
    """
    Represents a knowledge graph
    """
    def __init__(self):
        """
        Initalize graph with nodes
        """
        self.atoms = {}

    def atom(self, name, *args, **kwargs):
        """
        if an atom with name already exists, return it
        else create an Atom in this graph
        """
        atom = self.atoms.get(name, None)
        if atom is None:
            atom = node.Atom(name, self, *args, **kwargs)
            self.atoms[name] = atom
        return atom

    def entails(self, antecedent, concequent):
        """
        Connect antecedent and concequent
        TODO: Throws AtomNotInGraph if an atom in antecedent or
            concequent is not part of the graph
        """
        antecedent.outputs.append(concequent)
        concequent.inputs.append(antecedent)
        return concequent

    def eval(self, n, facts=[]):
        """
        Evaluate the truth value of node
            add node to graph and evaluate
        """
        for fact in facts:
            self.atoms[fact.name].tv = node.TRUE
        if isinstance(n, node.Atom):
            return n.eval()
        else:
            raise NotImplementedError()

    def __str__(self):
        strs = [str(atom) for atom in self.atoms.values()]
        return "Graph({})".format(strs)
