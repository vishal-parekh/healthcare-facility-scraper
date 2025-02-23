import os
from constants import (
    DEFAULT_LLM_PROVIDER,
    DEFAULT_INSTRUCTION_TO_LLM,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)

# Load the secret API key separately
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable not set")

# Optionally, you could override these constants with environment variables:
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", DEFAULT_LLM_PROVIDER)
INSTRUCTION_TO_LLM = os.environ.get("INSTRUCTION_TO_LLM", DEFAULT_INSTRUCTION_TO_LLM)
MAX_TOKENS = int(
    os.environ.get("MAX_TOKENS", DEFAULT_MAX_TOKENS)
)  # Provide default if needed
TEMPERATURE = float(os.environ.get("TEMPERATURE", DEFAULT_TEMPERATURE))

# Optionally you can combine these into a configuration dictionary
CONFIG = {
    "DEEPSEEK_API_KEY": DEEPSEEK_API_KEY,
    "LLM_PROVIDER": LLM_PROVIDER,
    "INSTRUCTION_TO_LLM": INSTRUCTION_TO_LLM,
    "MAX_TOKENS": MAX_TOKENS,
    "TEMPERATURE": TEMPERATURE,
}
