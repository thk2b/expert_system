import node
import error

class Graph:
    """
    Represents a knowledge graph
    Members:
        atoms: atomic facts that have a truth value
        closed: wether more atoms can curently be added to the graph
    """
    def __init__(self):
        self.atoms = {}
        self.closed = False

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

    def validate_atom(self, atom):
        if atom.graph is not self:
            raise error.AtomNotInGraph("{} belongs to another graph".format(atom))
        return atom

    def entails(self, antecedent, concequent):
        """
        Connect antecedent and concequent
        """
        antecedent.add_output(concequent)
        concequent.add_input(antecedent)

    def close(self, facts=[]):
        """
        Close the graph. 
        Set all atoms in facts to true, all others to their default value
        """
        if self.closed and facts:
            raise Exception("Graph is closed")
        self.closed = True
        for fact in facts:
            self.atoms[fact.name].tv = True

    def eval(self, n, facts=[], verbose=False):
        """
        Evaluate the truth value of node
            add node to graph and evaluate
        """
        self.close(facts)
        return n.eval(verbose=verbose)

    def reset(self):
        """
        Reset all atoms
        """
        for atom in self.atoms.values():
            atom.reset()
        self.closed = False

    def suppose(self, facts=[]):
        return Session(self, facts)

    def __str__(self):
        strs = [str(atom) for atom in self.atoms.values()]
        return "Graph({})".format(strs)

class Session:
    def __init__(self, graph, facts):
        self.graph = graph
        self.facts = facts

    def __enter__(self):
        self.graph.close(self.facts)

    def __exit__(self, *args):
        self.graph.reset()
