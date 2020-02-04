import abc


class IRule(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval_antecedent(self, input_vec):
        raise NotImplementedError


class CNFRule(IRule):
    def __init__(self, antecedent, consequent):
        self._antecedent = antecedent
        self._consequent = consequent

    def eval_antecedent(self, ling_vars, input_vec, logical_or_strat,
                        logical_and_strat):
        return self._antecedent.eval(ling_vars, input_vec, logical_or_strat,
                                     logical_and_strat)
