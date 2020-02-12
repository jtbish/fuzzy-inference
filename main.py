#!/usr/bin/python3
from domain import Domain
from membership_func import make_trapezoidal_membership_func as make_trap
from membership_func import make_triangular_membership_func as make_tri


def main():
    domain = Domain(0, 10)

    print("tri")
    tri = make_tri(domain, 0, 5, 10, "tri")
    print(tri.points)
    for i in range(0, 10 + 1):
        tri.fuzzify(i)

    print("\n")
    print("trap")
    trap = make_trap(domain, 0, 2.5, 7.5, 10, "trap")
    print(trap.points)
    for i in range(0, 10 + 1):
        trap.fuzzify(i)

    print("\n")
    print("tri2")
    tri2 = make_tri(domain, 2.5, 5, 7.5, "tri2")
    print(tri2.points)
    for i in range(0, 10 + 1):
        tri2.fuzzify(i)

    print("\n")
    print("trap2")
    trap2 = make_trap(domain, 2, 4, 6, 8, "trap2")
    print(trap2.points)
    for i in range(0, 10 + 1):
        trap2.fuzzify(i)

    print("\n")
    print("tri3")
    tri3 = make_tri(domain, 0, 0, 5, "tri3")
    print(tri3.points)
    for i in range(0, 10 + 1):
        tri3.fuzzify(i)

    print("\n")
    print("trap3")
    trap3 = make_trap(domain, 0, 0, 2.5, 5, "trap3")
    print(trap3.points)
    for i in range(0, 10 + 1):
        trap3.fuzzify(i)
    print(trap3._polygon.area)
    print(trap3._polygon.centroid)


if __name__ == "__main__":
    main()
