import abc

from sympy import Line, Piecewise, Point, Polygon
from sympy import oo as sympy_inf
from sympy import solve
from sympy.abc import x, y

RANGE_MIN = 0
RANGE_MAX = 1


class MembershipFuncABC(metaclass=abc.ABCMeta):
    """Fuzzy set / membership function."""
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
    def fuzzify(self, input_scalar):
        raise NotImplementedError


class PiecewiseLinearMembershipFunc(MembershipFuncABC):
    """Fuzzy set / membership function composed of a series of linear sections,
    e.g. triangle or trapezoid."""
    def __init__(self, domain, points, name):
        super().__init__(domain, name)
        self._points = points
        self._piecewise_func = self._create_piecewise_func(self._points)
        self._polygon = Polygon(*points)

    @property
    def points(self):
        return self._points

    @property
    def area(self):
        return abs(self._polygon.area)

    @property
    def centroid(self):
        return self._polygon.centroid

    def _create_piecewise_func(self, points):
        lines = self._create_lines_from_points(points)
        lines = self._remove_vertical_lines(lines)
        pieces = self._create_pieces(lines)
        return Piecewise(*pieces)

    def _create_lines_from_points(self, points):
        lines = []
        self._add_flat_line_at_domain_start_if_needed(points, lines)
        self._add_lines_for_given_points(points, lines)
        self._add_flat_line_at_domain_end_if_needed(points, lines)
        return lines

    def _add_flat_line_at_domain_start_if_needed(self, points, lines):
        first_point = points[0]
        assert first_point.y == RANGE_MIN
        flat_line_needed = first_point.x > self._domain.min
        if flat_line_needed:
            lines.append(Line(Point(self._domain.min, RANGE_MIN), first_point))

    def _add_lines_for_given_points(self, points, lines):
        line_lhs_points = points[:-1]
        line_rhs_points = points[1:]
        for (lhs_point, rhs_point) in zip(line_lhs_points, line_rhs_points):
            lines.append(Line(lhs_point, rhs_point))

    def _add_flat_line_at_domain_end_if_needed(self, points, lines):
        last_point = points[-1]
        assert last_point.y == RANGE_MIN
        flat_line_needed = last_point.x < self._domain.max
        if flat_line_needed:
            lines.append(Line(last_point, Point(self._domain.max, RANGE_MIN)))

    def _remove_vertical_lines(self, lines):
        return [line for line in lines if line.slope != sympy_inf]

    def _create_pieces(self, lines):
        pieces = []
        for line in lines:
            expr = line.equation(x, y)
            sub_domain_max = line.p2.x
            cond = x <= sub_domain_max
            pieces.append((expr, cond))
        return pieces

    def fuzzify(self, input_scalar):
        assert self._domain.min <= input_scalar <= self._domain.max

        eqn_to_solve = self._piecewise_func.subs(x, input_scalar)
        result = solve(eqn_to_solve, y)
        result_is_scalar = isinstance(result, list) and len(result) == 1
        assert result_is_scalar
        result = float(result[0])

        assert RANGE_MIN <= result <= RANGE_MAX
        return result

    def clip(self, truth_val):
        """Return a new membership function representing clipped version of
        this membership function."""
        clip_line = Line((0, truth_val), slope=0)
        cut_polygons = self._polygon.cut_section(clip_line)
        assert len(cut_polygons) == 2
        two_segments_created = None not in cut_polygons
        if two_segments_created:
            clipped_polygon = cut_polygons[1]  # lower polygon
        else:
            assert cut_polygons.count(None) == 1
            # get whichever one is not None
            for item in cut_polygons:
                if item is not None:
                    clipped_polygon = item
                    break
        return type(self)(domain=self._domain,
                          points=clipped_polygon.vertices,
                          name=f"{self._name}_clipped_{truth_val}")


def make_triangular_membership_func(domain, base_lhs_x, apex_x, base_rhs_x,
                                    name):
    assert domain.min <= base_lhs_x <= apex_x <= base_rhs_x <= domain.max

    points = [
        Point(base_lhs_x, RANGE_MIN),
        Point(apex_x, RANGE_MAX),
        Point(base_rhs_x, RANGE_MIN),
    ]
    return PiecewiseLinearMembershipFunc(domain, points, name)


def make_trapezoidal_membership_func(domain, bottom_base_lhs_x, top_base_lhs_x,
                                     top_base_rhs_x, bottom_base_rhs_x, name):
    assert domain.min <= bottom_base_lhs_x <= top_base_lhs_x <= \
            top_base_rhs_x <= bottom_base_rhs_x <= domain.max

    points = [
        Point(bottom_base_lhs_x, RANGE_MIN),
        Point(top_base_lhs_x, RANGE_MAX),
        Point(top_base_rhs_x, RANGE_MAX),
        Point(bottom_base_rhs_x, RANGE_MIN),
    ]
    return PiecewiseLinearMembershipFunc(domain, points, name)
