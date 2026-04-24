# run_optimized.py
from config import TARGET_INEQUALITIES
from pipeline import run_experiment


if __name__ == "__main__":
    run_experiment(TARGET_INEQUALITIES, prompt_variant="optimized")