# judge_agents.py
from dataclasses import dataclass
from enum import Enum
from textwrap import dedent
from typing import Dict

from gemini_client import call_judge
from inequalities import InequalitySpec


class JudgeLabel(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


@dataclass
class JudgeResult:
    label: JudgeLabel
    reason: str


def _parse_label_and_reason(raw: str) -> JudgeResult:
    """Simple parser: expect first line to contain ACCEPT/REJECT, rest is reason."""
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if not lines:
        return JudgeResult(JudgeLabel.REJECT, "Empty judge response")

    first = lines[0].upper()
    if "ACCEPT" in first:
        label = JudgeLabel.ACCEPT
    else:
        label = JudgeLabel.REJECT

    reason = "\n".join(lines[1:]) if len(lines) > 1 else ""
    return JudgeResult(label=label, reason=reason)


FINAL_ANSWER_PROMPT = dedent(
    """
    You are a strict mathematical proof checker.

    You are given an inequality, its domain, and a proposed proof written in natural language.

    Your task:
    1. Decide whether the proof correctly establishes the inequality for all variables in the stated domain.
    2. Pay attention to whether the final conclusion matches the original inequality.
    3. Ignore minor stylistic issues; focus on logical validity and correctness.

    Respond in the following format:
    - First line: either "ACCEPT" or "REJECT".
    - Subsequent lines: a brief explanation of your decision.

    Inequality statement: {statement}
    Domain: {domain}

    Proof:
    {proof}
    """
)


TOY_CASE_PROMPT = dedent(
    """
    You are a judge for mathematical proofs of inequalities.

    Given the inequality, its domain, and a proposed proof, determine whether the proof improperly relies
    on a small number of specific numerical examples ("toy cases") instead of a general argument.

    A proof should be REJECTED if it only checks a few sample values or relies on a diagram or plot
    without proving the statement for all allowed values.

    Respond in the following format:
    - First line: "ACCEPT" if the proof is fully general; "REJECT" if it is toy-case based.
    - Subsequent lines: a short explanation.

    Inequality statement: {statement}
    Domain: {domain}

    Proof:
    {proof}
    """
)


LOGICAL_GAP_PROMPT = dedent(
    """
    You are a logical consistency judge for inequality proofs.

    Examine the proof step by step and decide whether there are logical gaps:
    - missing justifications for non-obvious steps
    - unjustified implications (e.g., assuming what needs to be proved)
    - invalid use of known inequalities or theorems.

    Respond in the following format:
    - First line: "ACCEPT" if there are no significant logical gaps; otherwise "REJECT".
    - Subsequent lines: briefly describe any gaps you find.

    Inequality statement: {statement}
    Domain: {domain}

    Proof:
    {proof}
    """
)


APPROXIMATION_PROMPT = dedent(
    """
    You are a numerical approximation judge for inequality proofs.

    Decide whether the proof uses approximations (e.g., replacing expressions by approximate decimal values)
    in a way that could invalidate the inequality or hide errors.

    Respond in the following format:
    - First line: "ACCEPT" if all approximations are clearly justified and safe; otherwise "REJECT".
    - Subsequent lines: explain any problematic approximations.

    Inequality statement: {statement}
    Domain: {domain}

    Proof:
    {proof}
    """
)


COMPUTATION_PROMPT = dedent(
    """
    You are an arithmetic and algebraic computation judge for inequality proofs.

    Inspect the derivations and check for incorrect algebraic manipulations, sign errors, or arithmetic mistakes
    that could affect the validity of the conclusion.

    Respond in the following format:
    - First line: "ACCEPT" if computations appear correct; otherwise "REJECT".
    - Subsequent lines: describe any computational errors.

    Inequality statement: {statement}
    Domain: {domain}

    Proof:
    {proof}
    """
)


def _run_judge(prompt_template: str, ineq: InequalitySpec, proof: str) -> JudgeResult:
    prompt = prompt_template.format(
        statement=ineq.statement,
        domain=ineq.domain,
        proof=proof,
    )
    raw = call_judge(prompt)
    return _parse_label_and_reason(raw)


def run_all_judges(ineq: InequalitySpec, proof: str) -> Dict[str, JudgeResult]:
    results = {
        "final": _run_judge(FINAL_ANSWER_PROMPT, ineq, proof),
        "toy_case": _run_judge(TOY_CASE_PROMPT, ineq, proof),
        "logical_gap": _run_judge(LOGICAL_GAP_PROMPT, ineq, proof),
        "approximation": _run_judge(APPROXIMATION_PROMPT, ineq, proof),
        "computation": _run_judge(COMPUTATION_PROMPT, ineq, proof),
    }
    return results


def overall_pass(results: Dict[str, JudgeResult]) -> bool:
    return all(r.label == JudgeLabel.ACCEPT for r in results.values())