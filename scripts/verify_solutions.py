"""SymPy gate: every "check your result" claim in the book becomes an expression that must be zero.

Each transcription group writes its own plug-in file (checks/checks_<group>.py) with a
`build(ctx)` function. The gate loads all plug-ins, tests every expression and exits
with status 1 if any claim fails. A self-test proves the gate can actually reject wrong
claims; without it, "all checks passed" would mean nothing.

Usage:
    python -I scripts/verify_solutions.py --checks-dir examples/numeric-branch/checks
    python -I scripts/verify_solutions.py --selftest

Plug-in contract:
    def build(ctx):
        ctx["add"](question_id, description, expression, samples=None)
    ctx provides: add, sp (sympy), x, C, C1, C2.

What it does and does not prove:
    It proves that the stated result satisfies the equation. It does NOT prove that the
    transcription matches the handwritten page; that is the job of the two independent
    readings and the page-by-page audit (see docs/quality-assurance.md).

Requires: sympy.
"""

from __future__ import annotations

import argparse
import importlib.util
import random
import sys
from pathlib import Path

import sympy as sp

x = sp.symbols("x", real=True)
C, C1, C2 = sp.symbols("C C1 C2", real=True)
DEFAULT_SAMPLES = {x: (0.5, 2.0), C: (-2, 2), C1: (-2, 2), C2: (-2, 2)}


def is_zero(expr, samples) -> tuple[bool, str]:
    """Symbolic zero test first; if inconclusive, evaluate at 12 seeded random points."""
    e = sp.simplify(expr)
    if e == 0:
        return True, "symbolic"
    rng = random.Random(0)
    for _ in range(12):
        point = {s: rng.uniform(lo, hi) for s, (lo, hi) in samples.items()}
        value = complex(sp.N(e.subs(point)))
        if abs(value) > 1e-8:
            return False, f"residual {value:.3g}"
    return True, "numeric"


def load_checks(checks_dir: Path) -> list[tuple]:
    checks = []

    def add(qid, desc, expr, samples=None):
        checks.append((qid, desc, expr, samples or DEFAULT_SAMPLES))

    ctx = dict(add=add, sp=sp, x=x, C=C, C1=C1, C2=C2)
    plugins = sorted(checks_dir.glob("checks_*.py"))
    if not plugins:
        raise FileNotFoundError(f"no checks_*.py plug-ins in {checks_dir}")
    for f in plugins:
        spec = importlib.util.spec_from_file_location(f.stem, f)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.build(ctx)
    return checks


def run(checks_dir: Path) -> int:
    failed = 0
    checks = load_checks(checks_dir)
    for qid, desc, expr, samples in checks:
        ok, how = is_zero(expr, samples)
        failed += not ok
        print(f"{qid:8} {desc:<44} {'OK' if ok else 'FAIL':4}  {how}")
    print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
    return failed


def selftest() -> int:
    """The gate must reject known-wrong claims."""
    wrong = {
        "sign error: (C sin x)' + C cos x": sp.diff(C * sp.sin(x), x) + C * sp.cos(x),
        "wrong equation: y'' - y for y = C1 sin x + C2 cos x":
            sp.diff(C1 * sp.sin(x) + C2 * sp.cos(x), x, 2) - (C1 * sp.sin(x) + C2 * sp.cos(x)),
        "dropped constant: y = 2 + e^(-2x) vs y' + 2y = 5": sp.diff(2 + sp.exp(-2 * x), x) + 2 * (2 + sp.exp(-2 * x)) - 5,
    }
    samples = {x: (0.3, 2.0), C: (1, 2), C1: (1, 2), C2: (1, 2)}
    missed = 0
    for name, expr in wrong.items():
        caught = not is_zero(expr, samples)[0]
        missed += not caught
        print(f"{'caught' if caught else 'MISSED'}  {name}")
    print(f"\nself-test: {len(wrong) - missed}/{len(wrong)} wrong claims rejected")
    return missed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--checks-dir", type=Path, default=Path("checks"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    return 1 if (selftest() if args.selftest else run(args.checks_dir)) else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
