from pathlib import Path

# Core paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Use OpenRouter's strictly FREE Gemini endpoints to bypass the 402 Error
GEMINI_MODEL_PROVER = "google/gemini-2.0-flash:free"   
GEMINI_MODEL_JUDGE = "google/gemini-2.0-flash:free"            

# Generation parameters
MAX_TOKENS = 256
TEMPERATURE_BASELINE = 0.7
TEMPERATURE_STRICT = 0.2

# Experiment configuration
NUM_SAMPLES_PER_INEQ = 5 

# Inequalities to study
TARGET_INEQUALITIES = ["cauchy_schwarz", "jensen"]