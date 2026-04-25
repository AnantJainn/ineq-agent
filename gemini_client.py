# import os
# from openai import OpenAI
# from config import GEMINI_MODEL_PROVER, GEMINI_MODEL_JUDGE, MAX_TOKENS

# # Initialize OpenAI client pointing to OpenRouter's endpoint
# api_key = os.environ.get("OPENROUTER_API_KEY")
# if not api_key:
#     raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=api_key,
# )

# def call_gemini(
#     prompt: str,
#     model: str,
#     temperature: float = 0.7,
#     system_instruction: str | None = None,
# ) -> str:
#     """Single-turn helper that returns plain text using OpenRouter."""
#     messages = []
    
#     if system_instruction is not None:
#         messages.append({"role": "system", "content": system_instruction})
        
#     messages.append({"role": "user", "content": prompt})

#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         max_tokens=MAX_TOKENS,
#         # OpenRouter recommends passing these headers
#         extra_headers={
#             "HTTP-Referer": "https://github.com/anantjainn/ineq-agent",
#             "X-Title": "IneqAgent",
#         }
#     )

#     return response.choices[0].message.content.strip()

# def call_prover(prompt: str, temperature: float = 0.7) -> str:
#     return call_gemini(prompt, model=GEMINI_MODEL_PROVER, temperature=temperature)

# def call_judge(prompt: str, temperature: float = 0.2) -> str:
#     return call_gemini(prompt, model=GEMINI_MODEL_JUDGE, temperature=temperature)







import os
import time
from openai import OpenAI, RateLimitError

from config import GEMINI_MODEL_PROVER, GEMINI_MODEL_JUDGE, MAX_TOKENS

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def call_gemini(
    prompt: str,
    model: str,
    temperature: float = 0.7,
    system_instruction: str | None = None,
) -> str:
    messages = []
    
    if system_instruction is not None:
        messages.append({"role": "system", "content": system_instruction})
        
    messages.append({"role": "user", "content": prompt})

    # Robust Retry Loop to handle 429 Errors gracefully
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=MAX_TOKENS,
                extra_headers={
                    "HTTP-Referer": "https://github.com/anantjainn/ineq-agent",
                    "X-Title": "IneqAgent",
                }
            )
            # Add a mandatory delay between successful calls to be kind to free APIs
            time.sleep(2) 
            return response.choices[0].message.content.strip()
            
        except RateLimitError as e:
            print(f"[!] Rate limited by API. Sleeping 5 seconds... (Attempt {attempt+1}/{max_retries})")
            time.sleep(5)
        except Exception as e:
            print(f"[!] Unexpected error: {e}. Sleeping 3 seconds...")
            time.sleep(3)

    return "ERROR: Failed to generate response after maximum retries."

def call_prover(prompt: str, temperature: float = 0.7) -> str:
    return call_gemini(prompt, model=GEMINI_MODEL_PROVER, temperature=temperature)

def call_judge(prompt: str, temperature: float = 0.2) -> str:
    return call_gemini(prompt, model=GEMINI_MODEL_JUDGE, temperature=temperature)