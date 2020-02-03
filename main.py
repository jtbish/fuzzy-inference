#!/usr/bin/python3
from membership_function import TrapezoidalMembershipFunc as Trap
from membership_function import TriangularMembershipFunc as Tri


def main():
    print("tri")
    tri = Tri(0, 5, 10)
    print(tri._point_path)
    for i in range(0, 10 + 1):
        tri.fuzzify(i)

    print("\n")
    print("trap")
    trap = Trap(0, 2.5, 7.5, 10)
    print(trap._point_path)
    for i in range(0, 10 + 1):
        trap.fuzzify(i)

    print("\n")
    print("tri2")
    tri2 = Tri(2.5, 5, 7.5)
    print(tri2._point_path)
    for i in range(0, 10 + 1):
        tri2.fuzzify(i)

    print("\n")
    print("trap2")
    trap2 = Trap(2, 4, 6, 8)
    print(trap2._point_path)
    for i in range(0, 10 + 1):
        trap2.fuzzify(i)

    print("\n")
    print("tri3")
    tri3 = Tri(0, 0, 5)
    print(tri3._point_path)
    for i in range(0, 10 + 1):
        tri3.fuzzify(i)

    print("\n")
    print("trap3")
    trap3 = Trap(0, 0, 2.5, 5)
    print(trap3._point_path)
    for i in range(0, 10 + 1):
        trap3.fuzzify(i)


if __name__ == "__main__":
    main()
