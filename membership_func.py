import abc

from collections import OrderedDict, namedtuple

RANGE_MIN = 0
RANGE_MAX = 1

Domain = namedtuple("Domain", ["min", "max"])


def _make_copy_without_dups(seq):
    return list(OrderedDict.fromkeys(seq))


class MembershipFuncABC(metaclass=abc.ABCMeta):
    def __init__(self, domain, name):
        self._domain = domain
        self._name = name

    @property
    def domain(self):
        return self._domain

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def fuzzify(self, input_):
        raise NotImplementedError


class PiecewiseLinearMembershipFunc(MembershipFuncABC):
    def __init__(self, domain, point_path, name):
        super().__init__(domain, name)
        self._point_path = _make_copy_without_dups(point_path)
        self._validate_point_path(self._domain, self._point_path)
        self._piecewise_func = self._create_piecewise_func(self._point_path)

    @property
    def point_path(self):
        return self._point_path

    def _validate_point_path(self, domain, point_path):
        self._check_points_are_in_ascending_x_order(point_path)
        self._check_points_are_in_domain(domain, point_path)
        self._check_points_are_in_range(point_path)

    def _check_points_are_in_ascending_x_order(self, point_path):
        for first_point, second_point in zip(point_path[:-1], point_path[1:]):
            assert first_point.x <= second_point.x

    def _check_points_are_in_domain(self, domain, point_path):
        for point in point_path:
            assert domain.min <= point.x <= domain.max

    def _check_points_are_in_range(self, point_path):
        for point in point_path:
            assert RANGE_MIN <= point.y <= RANGE_MAX

    def _create_piecewise_func(self, point_path):
        piece_lhs_points = point_path[:-1]
        piece_rhs_points = point_path[1:]
        piecewise_func = []
        for (piece_lhs_point, piece_rhs_point) in zip(piece_lhs_points,
                                                      piece_rhs_points):
            piecewise_func.append(LinearFunc(piece_lhs_point, piece_rhs_point))
        return piecewise_func

    def fuzzify(self, input_):
        piece_outputs = self._calc_raw_piece_outputs(input_)
        piece_outputs = _make_copy_without_dups(piece_outputs)
        has_single_output = len(piece_outputs) == 1
        assert has_single_output
        output = piece_outputs[0]
        return output

    def _calc_raw_piece_outputs(self, input_):
        outputs = []
        for piece in self._piecewise_func:
            try:
                output = piece(input_)
            except ValueError:
                continue
            else:
                outputs.append(output)
        return outputs


def make_triangular_membership_func(domain, base_lhs, apex, base_rhs, name):
    point_path = [
        Point(domain.min, RANGE_MIN),
        Point(base_lhs, RANGE_MIN),
        Point(apex, RANGE_MAX),
        Point(base_rhs, RANGE_MIN),
        Point(domain.max, RANGE_MIN)
    ]
    return PiecewiseLinearMembershipFunc(domain, point_path, name)


def make_trapezoidal_membership_func(domain, bottom_base_lhs, top_base_lhs,
                                     top_base_rhs, bottom_base_rhs, name):
    point_path = [
        Point(domain.min, RANGE_MIN),
        Point(bottom_base_lhs, RANGE_MIN),
        Point(top_base_lhs, RANGE_MAX),
        Point(top_base_rhs, RANGE_MAX),
        Point(bottom_base_rhs, RANGE_MIN),
        Point(domain.max, RANGE_MIN)
    ]
    return PiecewiseLinearMembershipFunc(domain, point_path, name)


Point = namedtuple("Point", ["x", "y"])


class LinearFunc:
    """Function that defines a straight line between the LHS and RHS
    points.

    Used as part of a piecewise function definition for a membership
    function."""
    def __init__(self, lhs_point, rhs_point):
        self._lhs_point = lhs_point
        self._rhs_point = rhs_point
        self._grad = self._calc_grad(y2=self._rhs_point.y,
                                     y1=self._lhs_point.y,
                                     x2=self._rhs_point.x,
                                     x1=self._lhs_point.x)

    def _calc_grad(self, y2, y1, x2, x1):
        try:
            return (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            return None

    def __call__(self, input_):
        self._check_input_is_in_sub_domain(input_)
        return self._calc_output(input_)

    def _check_input_is_in_sub_domain(self, input_):
        if not (self._lhs_point.x <= input_ <= self._rhs_point.x):
            raise ValueError(f"Input {input_} not in sub-domain")

    def _calc_output(self, input_):
        if self._grad is not None:
            result = self._interpolate_along_line_for_defined_grad(input_)
        else:
            result = self._take_max_y_val_for_undefined_grad()
        assert RANGE_MIN <= result <= RANGE_MAX
        return result

    def _interpolate_along_line_for_defined_grad(self, input_):
        y2 = None
        y1 = self._lhs_point.y
        x2 = input_
        x1 = self._lhs_point.x

        y2 = self._grad * (x2 - x1) + y1
        return y2

    def _take_max_y_val_for_undefined_grad(self):
        has_undefined_grad = self._lhs_point.x == self._rhs_point.x
        assert has_undefined_grad
        return max(self._lhs_point.y, self._rhs_point.y)
