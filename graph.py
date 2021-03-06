import node
import error

class Graph:
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
        """
        if antecedent is concequent:
            raise ValueError('concequent must be different than antecedent')
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

    def close(self, facts=[]):
        """
        Close the graph. 
        Set all leaf atoms to false if indeterminate, set all atoms in facts to true.
        """
        if self.closed and facts:
            raise Exception("Graph is closed")
        self.closed = True
        for fact in facts:
            self.atoms[fact.name].tv = node.TRUE
        for atom in set(self.atoms.values()).difference(set(facts)):
            if len(atom.inputs) == 0 and atom.tv == node.INDETERMINATE:
                atom.tv = node.FALSE

    def eval(self, n, facts=[], verbose=False):
        """
        Evaluate the truth value of node
            add node to graph and evaluate
        """
        self.close(facts)
        return n.eval(None, verbose=verbose)

    def reset(self):
        """
        Reset facts to their orignial truth value or indeterminate
        """
        for atom in self.atoms.values():# TODO: Atom.reset()
            atom.tv = atom.original_tv if atom.original_tv is not None else node.INDETERMINATE
            if atom.tv_reason:
                atom.tv_reason = None
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
