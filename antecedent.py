class CNFAntecedentElem:
    """Mask of allele bits connected via disjunction (OR) operator."""
    def __init__(self, allele_mask):
        self._allele_mask

    def eval(self, ling_var, input_, logical_or_strat):
        result = []
        for (allele, membership_func) in zip(self._allele_mask,
                                             ling_var.membership_funcs):
            allele_is_active = allele == 1
            if allele_is_active:
                result.append(membership_func.fuzzify(input_))
        # TODO what if result is empty, or strat will blow up
        return logical_or_strat(result)


class CNFAntecedent:
    """Conjunction (AND) of allele masks for each input dimension."""
    def __init__(self, elems):
        self._elems = elems

    def eval(self, ling_vars, input_vec, logical_or_strat, logical_and_strat):
        result = []
        for (elem, ling_var, input_) in zip(self._elems, ling_vars, input_vec):
            result.append(elem.eval(ling_var, input_, logical_or_strat))
        return logical_and_strat(result)
