# prover_agent.py
from textwrap import dedent
from typing import Literal

from config import TEMPERATURE_BASELINE, TEMPERATURE_STRICT
from gemini_client import call_prover
from inequalities import INEQUALITIES, InequalitySpec

PromptVariant = Literal["baseline", "optimized"]


BASELINE_PROMPT_TEMPLATE = """You are a helpful math assistant.
Prove the following inequality in natural language:

Inequality: {statement}
Domain: {domain}

Write a proof.
"""


OPTIMIZED_PROMPT_TEMPLATE = dedent(
    """
    You are a rigorous mathematical assistant specializing in inequality proofs.

    Task:
    - Prove the inequality stated below.
    - Use a fully general argument (no reliance on a single numerical example).
    - Structure your proof into numbered steps.
    - In each step, explicitly state which theorem or algebraic rule you are using 
      (e.g., AM-GM, Cauchy–Schwarz, Jensen, linearity, non-negativity of squares).
    - Avoid unjustified approximations or hand-wavy arguments.

    Requirements:
    1. Begin with a clear restatement of the inequality and its domain.
    2. Provide a sequence of logically justified steps, numbered as "Step 1:", "Step 2:", etc.
    3. Do not rely on specific numeric toy cases; your argument must hold for all variables in the domain.
    4. Ensure that each transformation is valid and does not reverse inequality signs incorrectly.
    5. Conclude with a final sentence explicitly stating that the original inequality holds under the stated conditions.

    Inequality: {statement}
    Domain: {domain}
    Hint: {hint}

    Now write the complete proof.
    """
)


def build_prompt(ineq: InequalitySpec, variant: PromptVariant) -> str:
    if variant == "baseline":
        return BASELINE_PROMPT_TEMPLATE.format(
            statement=ineq.statement,
            domain=ineq.domain,
        )
    elif variant == "optimized":
        return OPTIMIZED_PROMPT_TEMPLATE.format(
            statement=ineq.statement,
            domain=ineq.domain,
            hint=ineq.hint,
        )
    else:
        raise ValueError(f"Unknown prompt variant: {variant}")


def generate_proof(ineq_key: str, variant: PromptVariant = "baseline") -> str:
    ineq = INEQUALITIES[ineq_key]
    prompt = build_prompt(ineq, variant)

    temperature = TEMPERATURE_BASELINE if variant == "baseline" else TEMPERATURE_STRICT
    return call_prover(prompt, temperature=temperature)