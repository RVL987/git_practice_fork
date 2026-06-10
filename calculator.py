def add(a, b):
    """Returns the sum of two numbers."""
    return a + b


def sub(a, b):
    """Returns the difference between two numbers."""
    return a - b


def mul(a, b):
    """Returns the product of two numbers."""
    return a * b


def div(a, b):
    """
    Returns the quotient of two numbers.
    Raises ValueError if denominator is zero.
    """
    if b != 0:
        return a / b
    else:
        raise ValueError("Division by 0 not possible")
