from collections import namedtuple

RANGE_MIN = 0
RANGE_MAX = 1

DOMAIN_MIN = 0
DOMAIN_MAX = 10


class MembershipFuncBase:
    def _create_piecewise_func(self, point_path):
        piece_lhs_points = point_path[:-1]
        piece_rhs_points = point_path[1:]
        pieces = []
        for (piece_lhs_point, piece_rhs_point) in zip(piece_lhs_points,
                                                      piece_rhs_points):
            if piece_lhs_point != piece_rhs_point:
                pieces.append(LinearFunction(piece_lhs_point, piece_rhs_point))
        return pieces

    def fuzzify(self, input_):
        output = []
        for piece in self._piecewise_func:
            output.append(piece(input_))
        # get rid of nones
        output = [val for val in output if val is not None]
        # get rid of dupes
        output = list(set(output))
        print(f"Fuzzy {input_} -> {output}")
        return output


class TriangularMembershipFunc(MembershipFuncBase):
    def __init__(self, base_lhs, apex, base_rhs):
        assert DOMAIN_MIN <= base_lhs <= apex <= base_rhs <= \
            DOMAIN_MAX

        self._base_lhs = base_lhs
        self._apex = apex
        self._base_rhs = base_rhs

        self._point_path = self._create_point_path()
        self._piecewise_func = self._create_piecewise_func(self._point_path)

    def _create_point_path(self):
        point_path = [
            Point(DOMAIN_MIN, RANGE_MIN),
            Point(self._base_lhs, RANGE_MIN),
            Point(self._apex, RANGE_MAX),
            Point(self._base_rhs, RANGE_MIN),
            Point(DOMAIN_MAX, RANGE_MIN)
        ]
        return point_path


class TrapezoidalMembershipFunc(MembershipFuncBase):
    def __init__(self, bottom_base_lhs, top_base_lhs, top_base_rhs,
                 bottom_base_rhs):
        assert DOMAIN_MIN <= bottom_base_lhs <= top_base_lhs <= \
            top_base_rhs <= bottom_base_rhs <= DOMAIN_MAX

        self._bottom_base_lhs = bottom_base_lhs
        self._top_base_lhs = top_base_lhs
        self._top_base_rhs = top_base_rhs
        self._bottom_base_rhs = bottom_base_rhs

        self._point_path = self._create_point_path()
        self._piecewise_func = self._create_piecewise_func(self._point_path)

    def _create_point_path(self):
        point_path = [
            Point(DOMAIN_MIN, RANGE_MIN),
            Point(self._bottom_base_lhs, RANGE_MIN),
            Point(self._top_base_lhs, RANGE_MAX),
            Point(self._top_base_rhs, RANGE_MAX),
            Point(self._bottom_base_rhs, RANGE_MIN),
            Point(DOMAIN_MAX, RANGE_MIN)
        ]
        return point_path


Point = namedtuple("Point", ["x", "y"])


class LinearFunction:
    """Function that defines a straight line between the LHS and RHS 'anchor'
    points.

    Used as part of a piecewise function definition for a membership
    function."""
    def __init__(self, lhs_anchor_point, rhs_anchor_point):
        self._lhs_anchor_point = lhs_anchor_point
        self._rhs_anchor_point = rhs_anchor_point

        y2 = self._rhs_anchor_point.y
        y1 = self._lhs_anchor_point.y
        x2 = self._rhs_anchor_point.x
        x1 = self._lhs_anchor_point.x

        try:
            self._grad = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            self._grad = None

    def __call__(self, input_):
        # TODO clean up
        if not (self._lhs_anchor_point.x <= input_ <=
                self._rhs_anchor_point.x):
            return None
        else:
            if self._grad is not None:
                result = self._interpolate_along_line_to_calc_y_val(input_)
            else:
                result = self._take_max_y_val_for_vertical_line()
            result = self._constrain_result_range(result)
            return result

    def _interpolate_along_line_to_calc_y_val(self, input_):
        y2 = None
        y1 = self._lhs_anchor_point.y
        x2 = input_
        x1 = self._lhs_anchor_point.x

        y2 = self._grad * (x2 - x1) + y1
        return y2

    def _take_max_y_val_for_vertical_line(self):
        assert self._lhs_anchor_point.x == self._rhs_anchor_point.x
        return max(self._lhs_anchor_point.y, self._rhs_anchor_point.y)

    def _constrain_result_range(self, result):
        result = max(result, RANGE_MIN)
        result = min(result, RANGE_MAX)
        return result
