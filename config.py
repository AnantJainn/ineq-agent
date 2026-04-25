# from pathlib import Path

# # Core paths
# PROJECT_ROOT = Path(__file__).parent
# OUTPUT_DIR = PROJECT_ROOT / "outputs"
# OUTPUT_DIR.mkdir(exist_ok=True)

# # Use OpenRouter's strictly FREE Gemini endpoints to bypass the 402 Error
# GEMINI_MODEL_PROVER = "google/gemma-4-31b-it:free"   
# GEMINI_MODEL_JUDGE = "google/gemma-4-31b-it:free"            

# # Generation parameters
# MAX_TOKENS = 256
# TEMPERATURE_BASELINE = 0.7
# TEMPERATURE_STRICT = 0.2

# # Experiment configuration
# NUM_SAMPLES_PER_INEQ = 5 

# # Inequalities to study
# TARGET_INEQUALITIES = ["cauchy_schwarz", "jensen"]








from pathlib import Path

# Core paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Using a highly available, lightweight free model
GEMINI_MODEL_PROVER = "google/gemma-4-31b-it"   
GEMINI_MODEL_JUDGE = "google/gemma-4-31b-it"            

# Generation parameters
MAX_TOKENS = 2048
TEMPERATURE_BASELINE = 0.7
TEMPERATURE_STRICT = 0.2

# REDUCED TO 1 FOR TESTING: This prevents massive bursts of requests
NUM_SAMPLES_PER_INEQ = 1 

# REDUCED TO 1 INEQUALITY FOR TESTING
TARGET_INEQUALITIES = ["cauchy_schwarz"]