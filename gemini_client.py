# gemini_client.py
import os
from typing import List

from google import genai
from google.genai import types as genai_types

from config import GEMINI_MODEL_PROVER, GEMINI_MODEL_JUDGE, MAX_TOKENS

# Initialize client: picks up GEMINI_API_KEY or GOOGLE_API_KEY from environment.
client = genai.Client()


def call_gemini(
    prompt: str,
    model: str,
    temperature: float = 0.7,
    system_instruction: str | None = None,
) -> str:
    """Single-turn helper that returns plain text from Gemini."""
    parts: List[genai_types.Part] = [genai_types.Part.from_text(text=prompt)]

    config = genai_types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=MAX_TOKENS,
    )

    # System-like instruction goes into the config or prefix if desired.
    if system_instruction is not None:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=model,
        contents=parts,
        config=config,
    )

    return getattr(response, "text", "").strip()


def call_prover(prompt: str, temperature: float = 0.7) -> str:
    return call_gemini(prompt, model=GEMINI_MODEL_PROVER, temperature=temperature)


def call_judge(prompt: str, temperature: float = 0.2) -> str:
    return call_gemini(prompt, model=GEMINI_MODEL_JUDGE, temperature=temperature)