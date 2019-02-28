import node
import error

class Graph:
    """
    Represents a knowledge graph
    """
    def __init__(self):
        """
        Initalize graph with nodes
        """
        self.atoms = {}
        self.locked = False

    def atom(self, name, *args, **kwargs):
        """
        if an atom with name already exists, return it
        else create an Atom in this graph
        """
        atom = self.atoms.get(name, None)
        if atom is None:
            atom = node.Atom(name, self, *args, **kwargs)
            self.atoms[name] = atom
        elif kwargs.get('tv', None):
            raise ValueError('cannot specify atom.tv when the atom already exists')
        return atom

    def validate_atom(self, atom):
        if atom.graph is not self:
            raise error.AtomNotInGraph("{} belongs to another graph".format(atom))
        return atom

    def entails(self, antecedent, concequent):
        """
        Connect antecedent and concequent
        TODO: Throws AtomNotInGraph if an atom in antecedent or
            concequent is not part of the graph
        """
        if isinstance(antecedent, node.Atom):
            self.validate_atom(antecedent)
            antecedent.outputs.append(concequent) #FIXME: check if concequent is a valid atom
        else:
            antecedent.output = concequent
        if isinstance(concequent, node.Atom):
            self.validate_atom(concequent)
            concequent.inputs.append(antecedent)
        else:
            concequent.input = antecedent
        return concequent

    def lock(self, facts=[]):
        """Temporary lock to prevent contradictions in eval"""
        if self.locked and facts:
            raise Exception("Graph is locked")
        self.locked = True
        for fact in facts:
            self.atoms[fact.name].tv = node.TRUE

    def eval(self, n, facts=[]):
        """
        Evaluate the truth value of node
            add node to graph and evaluate
        """
        self.lock(facts)
        if isinstance(n, node.Atom):
            return n.eval()
        else:
            raise NotImplementedError()

    def __str__(self):
        strs = [str(atom) for atom in self.atoms.values()]
        return "Graph({})".format(strs)
