import abc


class IInferenceEngine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def process(self, input_vec):
        raise NotImplementedError


class FATIEngine:
    def __init__(self, ling_vars, logical_or_strat, logical_and_strat,
                 implication_strat, aggregation_strat, rule_base):
        self._ling_vars = ling_vars
        self._logical_or_strat = logical_or_strat
        self._logical_and_strat = logical_and_strat
        self._implication_strat = implication_strat
        self._aggregation_strat = aggregation_strat
        self._rule_base = rule_base

    def process(self, input_vec):
        rule_antecedent_outputs = \
            self._collect_rule_antecedent_outputs(input_vec)
        implication_outputs = \
            self._perform_implication(
                    rule_antecedent_outputs)
        aggregated_consequents = \
            self._aggregate_consequents(implication_outputs)
        return self._deffuzify(aggregated_consequents)

    def _collect_rule_antecedent_outputs(self, input_vec):
        rule_antecedent_outputs = []
        for rule in self._rule_base:
            rule_antecedent_outputs.append(
                rule.eval_antecedent(self._ling_vars, input_vec,
                                     self._logical_or_strat,
                                     self._logical_and_strat))
        return rule_antecedent_outputs

    def _perform_implication(self, rule_antecedent_outputs):
        pass

    def _aggregate_consequents(self, implication_outputs):
        pass

    def _defuzzify(self, aggregated_consequents):
        pass
