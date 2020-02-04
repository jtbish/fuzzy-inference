#!/usr/bin/python3
from membership_function import Domain
from membership_function import make_trapezoidal_membership_func as make_trap
from membership_function import make_triangular_membership_func as make_tri


def main():
    domain = Domain(0, 10)

    print("tri")
    tri = make_tri(domain, 0, 5, 10)
    print(tri._point_path)
    for i in range(0, 10 + 1):
        tri.fuzzify(i)

    print("\n")
    print("trap")
    trap = make_trap(domain, 0, 2.5, 7.5, 10)
    print(trap._point_path)
    for i in range(0, 10 + 1):
        trap.fuzzify(i)

    print("\n")
    print("tri2")
    tri2 = make_tri(domain, 2.5, 5, 7.5)
    print(tri2._point_path)
    for i in range(0, 10 + 1):
        tri2.fuzzify(i)

    print("\n")
    print("trap2")
    trap2 = make_trap(domain, 2, 4, 6, 8)
    print(trap2._point_path)
    for i in range(0, 10 + 1):
        trap2.fuzzify(i)
    trap2.plot()

    print("\n")
    print("tri3")
    tri3 = make_tri(domain, 0, 0, 5)
    print(tri3._point_path)
    for i in range(0, 10 + 1):
        tri3.fuzzify(i)

    print("\n")
    print("trap3")
    trap3 = make_trap(domain, 0, 0, 2.5, 5)
    print(trap3._point_path)
    for i in range(0, 10 + 1):
        trap3.fuzzify(i)


if __name__ == "__main__":
    main()
