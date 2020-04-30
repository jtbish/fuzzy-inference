class CNFAntecedent:
    """Antecedent representing AND of ORs, encoded as flat seq. of alleles."""
    def __init__(self, alleles, ling_vars):
        self._alleles = list(alleles)
        self._ling_vars = ling_vars
        self._check_alleles_are_valid_len(self._alleles, self._ling_vars)

    def _check_alleles_are_valid_len(self, alleles, ling_vars):
        total_membership_funcs = sum(
            [len(ling_var.membership_funcs) for ling_var in ling_vars])
        assert len(alleles) == total_membership_funcs

    def eval(self, input_vec, logical_or_strat, logical_and_strat):
        # TODO extract methods
        allele_idx = 0
        var_ress = []
        assert len(input_vec) == len(self._ling_vars)
        for (input_scalar, ling_var) in zip(input_vec, self._ling_vars):
            membership_ress = []
            for membership_func in ling_var.membership_funcs:
                allele = self._alleles[allele_idx]
                allele_is_active = allele == 1
                if allele_is_active:
                    membership_ress.append(
                        membership_func.fuzzify(input_scalar))
                else:
                    membership_ress.append(None)
                allele_idx += 1
            var_ress.append(logical_or_strat(membership_ress))
        assert allele_idx == len(self._alleles)
        # aggregate all var ress using logical and strat for overall truth val
        return logical_and_strat(var_ress)
