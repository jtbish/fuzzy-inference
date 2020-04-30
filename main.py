#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from antecedent import CNFAntecedent
from consequent import FuzzySetConsequent
from domain import Domain
from inference_engine import MamdaniEngine
from linguistic_var import LinguisticVar
from membership_func import make_triangular_membership_func as make_tri
from rule import CNFRule

matplotlib.use("Agg")


def main():
    x1_domain = Domain(0, 10)
    x1_l = make_tri(x1_domain, 0, 0, 3.5, "x1_l")
    x1_m = make_tri(x1_domain, 2.5, 5, 7.5, "x1_m")
    x1_h = make_tri(x1_domain, 6.5, 10, 10, "x1_h")

    x2_domain = Domain(0, 10)
    x2_l = make_tri(x2_domain, 0, 0, 3.5, "x2_l")
    x2_m = make_tri(x2_domain, 2.5, 5, 7.5, "x2_m")
    x2_h = make_tri(x2_domain, 6.5, 10, 10, "x2_h")

    y_domain = Domain(0, 10)
    y_l = make_tri(y_domain, 0, 0, 3.5, "y_l")
    y_m = make_tri(y_domain, 2.5, 5, 7.5, "y_m")
    y_h = make_tri(y_domain, 6.5, 10, 10, "y_h")

    x1 = LinguisticVar(membership_funcs=[x1_l, x1_m, x1_h], name="x1")
    x2 = LinguisticVar(membership_funcs=[x2_l, x2_m, x2_h], name="x2")
    y = LinguisticVar(membership_funcs=[y_l, y_m, y_h], name="y")

    engine = MamdaniEngine(input_ling_vars=[x1, x2], output_ling_var=y)

    rule_base = [
        # if (x1 is L OR M) AND (x2 is L) THEN (y is L)
        CNFRule(antecedent=CNFAntecedent(alleles=[1, 1, 0, 1, 0, 0],
                                         ling_vars=engine.input_ling_vars),
                consequent=FuzzySetConsequent(
                    allele=0, ling_var=engine.output_ling_var)),
        # if (x1 is M OR H) AND (x2 is H) THEN (y is H)
        CNFRule(antecedent=CNFAntecedent(alleles=[0, 1, 1, 0, 0, 1],
                                         ling_vars=engine.input_ling_vars),
                consequent=FuzzySetConsequent(
                    allele=2, ling_var=engine.output_ling_var)),
        # if (x1 is H) AND (x2 is L OR M) THEN (y is M)
        CNFRule(antecedent=CNFAntecedent(alleles=[0, 0, 1, 1, 1, 0],
                                         ling_vars=engine.input_ling_vars),
                consequent=FuzzySetConsequent(
                    allele=1, ling_var=engine.output_ling_var)),
        # if (x2 is L) THEN (y is L)
        CNFRule(antecedent=CNFAntecedent(alleles=[0, 0, 0, 1, 0, 0],
                                         ling_vars=engine.input_ling_vars),
                consequent=FuzzySetConsequent(
                    allele=0, ling_var=engine.output_ling_var)),
    ]

    x1s = np.arange(0.0, 10.0 + 0.1, 0.1)
    x2s = np.arange(0.0, 10.0 + 0.1, 0.1)
    ys = np.empty(shape=(len(x1s), len(x2s)))
    for x1_idx, x1 in enumerate(x1s):
        for x2_idx, x2 in enumerate(x2s):
            y = engine.process(rule_base, input_vec=[x1, x2])
            ys[x1_idx, x2_idx] = y

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    x1s, x2s = np.meshgrid(x1s, x2s)
    surf = ax.plot_surface(x1s, x2s, ys, cmap=cm.coolwarm)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("y")
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


if __name__ == "__main__":
    main()
