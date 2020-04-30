class FuzzySetConsequent:
    def __init__(self, allele, ling_var):
        self._allele = allele
        self._ling_var = ling_var
        self._check_allele_is_valid(self._allele, self._ling_var)

    def _check_allele_is_valid(self, allele, ling_var):
        # allele is coded as idx into membership funcs of ling var
        assert 0 <= allele < len(ling_var.membership_funcs)

    def eval(self, antecedent_truth):
        active_membership_func = self._ling_var.membership_funcs[self._allele]
        return active_membership_func.clip(antecedent_truth)
