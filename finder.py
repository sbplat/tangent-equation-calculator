import sympy as sp

MAX_NUMBER_THRESHOLD = sp.Number(1e-10)  # The max size of numbers to be considered zero.

x, y = sp.symbols("x y")  # Variables for the function, y is dependent on x.


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
    equation = sp.simplify(slope * x - slope * x_value + y_value)
    if exact:
        return equation
    else:
        return equation.evalf()


def on_function_line(function, dy_dx, x_input, y_input, exact, dbg_print):
    """
    Find the equation of a tangent line when the point is on the function.

    Args:
        function (sympy.Expr): The function.
        dy_dx (sympy.Expr): The derivative of the function.
        x_input (sympy.Number): The x value of the point.
        y_input (sympy.Number): The y value of the point.
        exact (bool): Whether to use exact values.
        dbg_print (bool): Whether to print debug information.

    Returns:
        sympy.Expr: The right-hand side of the tangent line equation.
    """
    slope = dy_dx.subs(x, x_input).subs(y, y_input)  # Determine the slope of the tangent.

    if dbg_print:
        print(f"The slope of the tangent is {slope}.")

    return build_line_equation(slope, x_input, y_input, exact)


def exterior_function_line(function, dy_dx, x_input, y_input, exact, dbg_print):
    """
    Find the equation of a tangent line when the point is exterior to the function.

    Args:
        function (sympy.Expr): The function.
        dy_dx (sympy.Expr): The derivative of the function.
        x_input (sympy.Number): The x value of the point.
        y_input (sympy.Number): The y value of the point.
        exact (bool): Whether to use exact values.
        dbg_print (bool): Whether to print debug information.

    Returns:
        List[x, y, sympy.Expr]: The x and y values of the point of intersection, and the right-hand side of the tangent line equation.
    """
    # Since the point is not on the curve, we need to solve for the point of tangency.
    # Let the point of tangency be (a, f(a)), where f is the function.
    a = sp.Symbol("a")  # Define the variable a.
    f_a_list = sp.solve(function.subs(x, a), y)  # Solve for f(a).

    # The slope of the tangent is dy/dx, so dy/dx = (f(a) - y) / (a - x).
    lhs_list = [dy_dx.subs(x, a).subs(y, f_a) for f_a in f_a_list]
    rhs_list = [(f_a - y_input) / (a - x_input) for f_a in f_a_list]

    # Solve for a.
    x_values = []
    for i in range(len(f_a_list)):
        lhs = lhs_list[i]
        rhs = rhs_list[i]
        for x_value in sp.solve(lhs - rhs, a):
            real, imag = x_value.as_real_imag()
            if imag < MAX_NUMBER_THRESHOLD:  # If the imaginary part is small enough, it is considered zero.
                x_values.append(real)

    compressed_points = [[x_i, sp.solve(function.subs(x, x_i), y)] for x_i in x_values]

    # Decompress the points.
    points = []
    for [x_i, y_points] in compressed_points:
        for y_i in y_points:
            points.append([x_i, y_i])

    if dbg_print:
        print(f"Point(s) of tangency: {', '.join([str(point).replace('[', '(').replace(']', ')') for point in points])}")

    rhs_equations = []

    for [x_i, y_i] in points:
        slope = dy_dx.subs(x, x_i).subs(y, y_i)

        # Check if the slope of the tangent and two points are equal.
        slope_2 = (y_i - y_input) / (x_i - x_input)
        if sp.Abs(slope - slope_2) > MAX_NUMBER_THRESHOLD:
            continue

        rhs_equations.append([x_i, y_i, build_line_equation(slope, x_i, y_i, exact)])

    return rhs_equations


if __name__ == "__main__":
    print("Tangent Line Equation Finder Using Derivatives")
    function = sp.sympify(input("Enter a function: "))
    dy_dx = sp.idiff(function, y, x)  # Find the derivative of y with respect to x.
    print(f"dy/dx = {dy_dx}")

    x_input = sp.sympify(input("Enter the x value: "))
    y_input = sp.sympify(input("Enter the y value: "))

    # Determine if the point is on the function.
    if function.subs(x, x_input).subs(y, y_input) == 0:
        print("The point is on the curve.")
        line_equation = on_function_line(function, dy_dx, x_input, y_input, True, True)
        print(f"The equation of the tangent line is y = {line_equation}.")
    else:
        print("The point is not on the curve.")
        rhs_equations = exterior_function_line(function, dy_dx, x_input, y_input, True, True)
        for [x_i, y_i, line_equation] in rhs_equations:
            print(f"The equation of the tangent at ({x_i}, {y_i}) is: y = {line_equation}.")
