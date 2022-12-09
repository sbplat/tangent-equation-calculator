import sympy as sp
import str_parser as parser

MAX_NUMBER_THRESHOLD = sp.Number(1e-10)  # The max size of numbers to be considered zero.

x, y = sp.symbols("x y")  # Variables for the function, y is dependent on x.

dbg_print = False
dbg = print if dbg_print else lambda *a, **k: None

class Line:
    """
    Represents information about a line.

    Attributes:
        slope (sympy.Number): The slope of the line.
        x_value (sympy.Number): The x value of the tangent point.
        y_value (sympy.Number): The y value of the tangent point.
        equation (sympy.Expr): The right-hand side of the equation of the line, where y is the left-hand side.
    """
    def __init__(self, slope, x_value, y_value, equation):
        self.slope = slope
        self.x_value = x_value
        self.y_value = y_value
        self.equation = equation

    @property
    def __dict__(self):
        return {
            "slope": str(self.slope),
            "x_value": str(self.x_value),
            "y_value": str(self.y_value),
            "equation": str(self.equation)
        }

def build_line_equation(slope, x_value, y_value, exact):
    """
    Build the equation of a line given the slope, x value, and y value.

    Args:
        slope (sympy.Number): The slope of the line.
        x_value (sympy.Number): The x value of the line.
        y_value (sympy.Number): The y value of the line.
        exact (bool): Whether to use exact values.

    Returns:
        sympy.Expr: The right-hand side of the line equation.
    """
    equation = None
    if slope == sp.zoo:  # Vertical line
        equation = sp.simplify(x - x_value)
    else:
        equation = sp.simplify(slope * x - y - slope * x_value + y_value)

    if exact:
        return equation
    else:
        return equation.evalf()

def on_function_line(function, dy_dx, x_input, y_input, exact):
    """
    Find the equation of a tangent line when the point is on the function.

    Args:
        function (sympy.Expr): The function.
        dy_dx (sympy.Expr): The derivative of the function.
        x_input (sympy.Number): The x value of the point.
        y_input (sympy.Number): The y value of the point.
        exact (bool): Whether to use exact values.

    Returns:
        Line: The tangent line.
    """
    slope = dy_dx.subs(x, x_input).subs(y, y_input)  # Determine the slope of the tangent.
    rhs_equation = build_line_equation(slope, x_input, y_input, exact)
    return Line(slope, x_input, y_input, rhs_equation)

def exterior_function_line(function, dy_dx, x_input, y_input, exact):
    """
    Find the equation of a tangent line when the point is exterior to the function.

    Args:
        function (sympy.Expr): The function.
        dy_dx (sympy.Expr): The derivative of the function.
        x_input (sympy.Number): The x value of the point.
        y_input (sympy.Number): The y value of the point.
        exact (bool): Whether to use exact values.

    Returns:
        List[Line]: The tangent lines.
    """
    # Since the point is not on the curve, we need to solve for the point of tangency.
    # Let the point of tangency be (a, f(a)), where f is the function.
    a = sp.Symbol("a")  # Define the variable a.
    f_a_list = sp.solve(function.subs(x, a), y)  # Solve for f(a).

    # The slope of the tangent is dy/dx, so dy/dx = (f(a) - y) / (a - x).
    lhs_list = [dy_dx.subs(x, a).subs(y, f_a) for f_a in f_a_list]
    rhs_list = [(f_a - y_input) / (a - x_input) for f_a in f_a_list]

    # Solve for a.
    x_values = set()
    for i in range(len(f_a_list)):
        lhs = lhs_list[i]
        rhs = rhs_list[i]
        for x_value in sp.solve(lhs - rhs, a, check=False):  # Avoid checking to keep vertical lines
            real, imag = x_value.as_real_imag()
            if imag < MAX_NUMBER_THRESHOLD:  # If the imaginary part is small enough, it is considered zero.
                x_values.add(real)

    points = []
    for x_i in x_values:
        y_values = list(sp.solve(function.subs(x, x_i), y))
        if exact:
            for y_i in y_values:
                points.append([x_i, y_i])
        else:
            for y_i in y_values:
                points.append([x_i.evalf(), y_i.evalf()])

    dbg("Point(s) of tangency (may contain extraneous points):")
    for point in points:
        dbg(f"({point[0]}, {point[1]})")

    lines = []

    for [x_i, y_i] in points:
        slope_1 = dy_dx.subs(x, x_i).subs(y, y_i)
        slope_2 = (y_i - y_input) / (x_i - x_input)

        # Check if the slope of the tangent and two points are equal.
        try:
            if sp.Abs(slope_1 - slope_2) > MAX_NUMBER_THRESHOLD:
                continue
        except TypeError as exception:
            # Edge case: The line is vertical.
            if not (slope_1 == sp.zoo and slope_2 == sp.zoo):
                continue

        rhs_equation = build_line_equation(slope_1, x_i, y_i, exact)
        lines.append(Line(slope_1, x_i, y_i, rhs_equation))

    return lines

def calculate(function, x_input, y_input, exact):
    """
    Calculate the equation of the tangent line.

    Args:
        function (sympy.Expr): The function.
        x_input (sympy.Number): The x value of the point.
        y_input (sympy.Number): The y value of the point.
        exact (bool): Whether to use exact values.

    Returns:
        sympy.Expr: dy/dx of the function.
        List[Line]: The tangent lines.
    """
    dy_dx = sp.idiff(function, y, x)  # Find the derivative of y with respect to x.

    lines = []

    # Determine if the point is on the function.
    if function.subs(x, x_input).subs(y, y_input) == 0:
        lines.append(on_function_line(function, dy_dx, x_input, y_input, exact))
    else:
        lines.extend(exterior_function_line(function, dy_dx, x_input, y_input, exact))

    return dy_dx, lines

if __name__ == "__main__":
    print("Tangent Line Equation Finder Using Derivatives")
    function = parser.parse(input("Enter a function in terms of x and y: 0 = "))
    x_input = parser.parse(input("Enter the x value of the point: "))
    y_input = parser.parse(input("Enter the y value of the point: "))
    exact = input("Type y to use exact values: ") == "y"

    dy_dx, lines = calculate(function, x_input, y_input, exact)
    print(f"The derivative of y with respect to x is {dy_dx}.")
    print("The tangent point(s) and line(s) is/are:")
    for line in lines:
        print(f"Tangent point: ({line.x_value}, {line.y_value})")
        print(f"{line.equation} = 0")
    if len(lines) == 0:
        print("No tangent line exists.")
