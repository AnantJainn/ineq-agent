# inequalities.py
from dataclasses import dataclass
from typing import Callable


@dataclass
class InequalitySpec:
    key: str
    name: str
    statement: str
    domain: str
    hint: str


INEQUALITIES: dict[str, InequalitySpec] = {}


def register(ineq: InequalitySpec) -> InequalitySpec:
    INEQUALITIES[ineq.key] = ineq
    return ineq


# a) Cauchy–Schwarz inequality
register(
    InequalitySpec(
        key="cauchy_schwarz",
        name="Cauchy–Schwarz Inequality",
        statement=(
            "For any real numbers a_1, …, a_n and b_1, …, b_n, "
            "we have (∑ a_i b_i)^2 ≤ (∑ a_i^2)(∑ b_i^2)."
        ),
        domain=(
            "All real n-tuples (a_1, …, a_n) and (b_1, …, b_n); "
            "you may assume n is a positive integer and sums are finite."
        ),
        hint=(
            "A standard proof considers the non-negativity of the quadratic polynomial "
            "in t given by ∑ (a_i t − b_i)^2 ≥ 0 and analyzes its discriminant."
        ),
    )
)

# c) Jensen's inequality for convex functions on R
register(
    InequalitySpec(
        key="jensen",
        name="Jensen's Inequality",
        statement=(
            "Let f be a convex function on an interval I ⊂ R, and let x_1, …, x_n ∈ I "
            "with weights λ_i ≥ 0 summing to 1. Then "
            "f(∑ λ_i x_i) ≤ ∑ λ_i f(x_i)."
        ),
        domain=(
            "Assume f is convex and real-valued on an interval I, each x_i lies in I, "
            "and λ_i ≥ 0 with ∑ λ_i = 1."
        ),
        hint=(
            "A common proof uses the definition of convexity as lying below its chords, "
            "or induction on n using the two-point convexity condition."
        ),
    )
)