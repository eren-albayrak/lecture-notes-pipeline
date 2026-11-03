"""SymPy plug-in for the synthetic example (examples/numeric-branch/main.typ).

Every expression must simplify to zero. Question IDs match the book (I.1, I.2).
In a real project each transcription group writes its own checks_<group>.py.
"""


def build(ctx):
    add, sp, x, C = ctx["add"], ctx["sp"], ctx["x"], ctx["C"]
    d = sp.diff

    # I.1  y' + 2y = 4  ->  y = 2 + C e^{-2x}
    y = 2 + C * sp.exp(-2 * x)
    add("I.1", "y = 2 + Ce^(-2x): y' + 2y - 4", d(y, x) + 2 * y - 4)
    add("I.1", "integrating factor: (y e^(2x))' - 4e^(2x)", d(y * sp.exp(2 * x), x) - 4 * sp.exp(2 * x))

    # I.2  y' = x y  ->  y = C e^{x^2/2}
    y = C * sp.exp(x**2 / 2)
    add("I.2", "y = Ce^(x^2/2): y' - x y", d(y, x) - x * y)
