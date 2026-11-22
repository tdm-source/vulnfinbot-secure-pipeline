import ast

def safe_calculation(user_input):
    # Parse Python literals without executing arbitrary code.
    value = ast.literal_eval(user_input)

    if type(value) not in (int, float):
        raise ValueError("Only numeric values are allowed.")

    return value
