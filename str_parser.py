import ast
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, convert_xor

transformations = standard_transformations + (convert_xor,)
sympy_defs = dir(sp)  # Get all sympy definitions

def is_safe(string):
    """
    Check if a string is safe for eval. This reduces the risk of arbitrary code execution, but may not catch all cases.

    Args:
        string (str): The string to check.

    Returns:
        bool: Whether the string is safe.
    """
    try:
        tree = ast.parse(string)
    except SyntaxError:
        return False
    disallowed = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
    for node in ast.walk(tree):
        flag = False
        if isinstance(node, disallowed):
            flag = True
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in sympy_defs:
                    # Example: abc(), abc(1, 2, 3), etc.
                    flag = True
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in sympy_defs:
                    # Example: abc.xyz(), abc.xyz(1, 2, 3), etc.
                    flag = True
            else:
                raise ValueError("Unknown function call type.")  # Should never happen
        if flag:
            return False
    return True

def parse(expr: str) -> sp.Expr:
    """
    Parse an arbitrary string into a sympy expression.

    Args:
        expr (str): The expression to parse.

    Returns:
        sympy.Expr: The parsed expression.

    Raises:
        ValueError: If the expression cannot be parsed correctly.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string.")

    if "=" in expr:
        raise ValueError("Expression must be all on one side of the equals sign.")

    # Check if the expression is safe for eval.
    if not is_safe(expr):
        raise ValueError("Expression is not safe.")

    try:
        return parse_expr(expr, transformations=transformations)
    except Exception as exception:
        raise ValueError("Sympy could not parse the expression.") from exception
