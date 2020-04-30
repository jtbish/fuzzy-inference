from logical_ops import logical_or_max, logical_and_min


class MamdaniEngine:
    def __init__(self, input_ling_vars, output_ling_var):
        self._input_ling_vars = input_ling_vars
        self._output_ling_var = output_ling_var
        self._logical_or_strat = logical_or_max
        self._logical_and_strat = logical_and_min

    @property
    def input_ling_vars(self):
        return self._input_ling_vars

    @property
    def output_ling_var(self):
        return self._output_ling_var

    def process(self, rule_base, input_vec):
        rule_outputs = []
        for rule in rule_base:
            rule_outputs.append(
                rule.eval(input_vec, self._logical_or_strat,
                          self._logical_and_strat))
        return self._defuzzify(rule_outputs)

    def _defuzzify(self, rule_outputs):
        # don't need to aggregate, just do area weighted avg of centroid x poss
        numerator = 0.0
        denominator = 0.0
        for fuzzy_set in rule_outputs:
            centroid_x_pos = float(fuzzy_set.centroid.x)
            numerator += float(fuzzy_set.area) * centroid_x_pos
            denominator += float(fuzzy_set.area)
        res = numerator / denominator
        return res
