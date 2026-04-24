# pipeline.py
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

from config import OUTPUT_DIR, NUM_SAMPLES_PER_INEQ
from inequalities import INEQUALITIES, InequalitySpec
from judge_agents import run_all_judges, overall_pass
from prover_agent import generate_proof, PromptVariant


@dataclass
class RunRecord:
    inequality_key: str
    prompt_variant: PromptVariant
    sample_id: int
    proof: str
    judge_results: dict
    overall_pass: bool


def run_experiment(
    inequality_keys: list[str],
    prompt_variant: PromptVariant,
    num_samples: int | None = None,
    log_path: Path | None = None,
) -> list[RunRecord]:
    if num_samples is None:
        num_samples = NUM_SAMPLES_PER_INEQ

    if log_path is None:
        log_path = OUTPUT_DIR / f"logs_{prompt_variant}.jsonl"

    records: list[RunRecord] = []

    with log_path.open("w", encoding="utf-8") as f:
        for key in inequality_keys:
            ineq: InequalitySpec = INEQUALITIES[key]
            for s in range(num_samples):
                proof = generate_proof(key, variant=prompt_variant)
                judge_results = run_all_judges(ineq, proof)
                rec = RunRecord(
                    inequality_key=key,
                    prompt_variant=prompt_variant,
                    sample_id=s,
                    proof=proof,
                    judge_results={k: asdict(v) for k, v in judge_results.items()},
                    overall_pass=overall_pass(judge_results),
                )
                records.append(rec)
                f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")

    return records