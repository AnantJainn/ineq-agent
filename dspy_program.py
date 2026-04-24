# dspy_program.py
import dspy

from inequalities import INEQUALITIES
from prover_agent import generate_proof


class ProveInequality(dspy.Signature):
    """Generate a step-by-step proof of an inequality."""

    inequality_key = dspy.InputField()
    proof = dspy.OutputField()


class ProverModule(dspy.Module):
    def __init__(self, instructions: str | None = None):
        super().__init__()
        # GEPA will evolve this instruction text.
        # It is prepended as a system-level hint to the prover prompt.
        self.instructions = instructions or (
            "You are a rigorous inequality-proof assistant. "
            "Always produce numbered, general proofs with explicit theorem usage."
        )
        self.predict = dspy.Predict(ProveInequality)

    def forward(self, inequality_key: str):
        # Call the underlying prover; GEPA will mutate self.instructions
        # which is injected inside generate_proof via a global or config if desired.
        proof_text = generate_proof(inequality_key, variant="optimized")
        return dspy.Prediction(proof=proof_text)