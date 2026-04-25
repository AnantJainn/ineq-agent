# optimize_with_gepa.py
import os
from typing import Optional

import dspy

from config import TARGET_INEQUALITIES
from dspy_program import ProverModule, ProveInequality
from inequalities import INEQUALITIES
from judge_agents import run_all_judges, overall_pass


# 1. Configure DSPy LMs.
#    Here, use an OpenRouter or other provider LM configured externally; in practice
#    you can also wrap Gemini in a dspy.LM-compatible interface if desired.

# Example (replace with your own LM configuration):
main_lm = dspy.LM("openai/sonar-reasoning", api_key=os.environ.get("PERPLEXITY_API_KEY"), api_base="https://api.perplexity.ai")
reflection_lm = dspy.LM("openai/sonar-pro", api_key=os.environ.get("PERPLEXITY_API_KEY"), api_base="https://api.perplexity.ai")
dspy.configure(lm=main_lm)


def build_train_val_sets():
    # For this project, every inequality key is a separate example.
    # You can create multiple copies with different random seeds if desired.
    examples = [
        dspy.Example(inequality_key=k).with_inputs("inequality_key")
        for k in TARGET_INEQUALITIES
    ]
    # Small dev/val split; with only a few inequalities, GEPA is almost in inference-time search mode.
    return examples, examples


def gepa_metric(
    example: dspy.Example,
    prediction: dspy.Prediction,
    trace=None,
    pred_name: Optional[str] = None,
    pred_trace=None,
) -> dspy.Prediction:
    """GEPA metric returning score and textual feedback based on judge results."""
    key = example["inequality_key"]
    ineq = INEQUALITIES[key]
    proof = prediction.proof

    results = run_all_judges(ineq, proof)
    passed = overall_pass(results)

    score = 1.0 if passed else 0.0

    # Build feedback text aggregating judge explanations.
    feedback_lines = [
        f"Overall_pass: {passed}",
    ]
    for jname, jres in results.items():
        feedback_lines.append(
            f"Judge {jname}: {jres.label} - {jres.reason}"
        )

    feedback = "\n".join(feedback_lines)
    return dspy.Prediction(score=score, feedback=feedback)


def main_gepa(reflection_lm: dspy.LM):
    train_set, val_set = build_train_val_sets()

    student = ProverModule()

    optimizer = dspy.GEPA(
        metric=gepa_metric,
        auto="light",
        reflection_lm=reflection_lm,
        num_threads=4,
        track_stats=True,
        track_best_outputs=True,
        add_format_failure_as_feedback=True,
    )

    optimized_program = optimizer.compile(
        student,
        trainset=train_set,
        valset=val_set,
    )

    # After optimization, inspect the evolved instructions
    print("Original instructions:", student.instructions)
    print("Optimized instructions:", optimized_program.instructions)

    # Optionally, run the optimized program to regenerate proofs and recompute metrics.
    for key in TARGET_INEQUALITIES:
        pred = optimized_program(inequality_key=key)
        print(f"Inequality {key}:\n", pred.proof)


if __name__ == "__main__":
    # You must instantiate reflection_lm according to your DSPy LM configuration.
    raise SystemExit(
        "Configure main and reflection LMs for DSPy, then call main_gepa(reflection_lm)."
    )