class CNFRule:
    def __init__(self, antecedent, consequent):
        self._antecedent = antecedent
        self._consequent = consequent

    def eval(self, input_vec, logical_or_strat, logical_and_strat):
        antecedent_truth = self._antecedent.eval(input_vec, logical_or_strat,
                                                 logical_and_strat)
        return self._consequent.eval(antecedent_truth)
