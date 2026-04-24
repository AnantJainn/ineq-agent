# config.py
from pathlib import Path

# Core paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini model configuration
# Use current, non-deprecated models per official guidance.
# GEMINI_MODEL_PROVER = "gemini-3-flash-preview"   # fast, good reasoning
# GEMINI_MODEL_JUDGE = "gemini-2.5-pro"            # stronger judge model
GEMINI_MODEL_PROVER = "gemini-1.5-flash"   
GEMINI_MODEL_JUDGE = "gemini-1.5-flash"
# Generation parameters
MAX_TOKENS = 4096
TEMPERATURE_BASELINE = 0.7
TEMPERATURE_STRICT = 0.2

# Experiment configuration
NUM_SAMPLES_PER_INEQ = 5  # how many stochastic proofs per inequality per setting

# Inequalities to study (strings must match keys in inequalities.py)
TARGET_INEQUALITIES = ["cauchy_schwarz", "jensen"]