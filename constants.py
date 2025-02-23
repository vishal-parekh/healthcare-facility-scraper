# constants.py
# This file holds non-sensitive configuration constants.
# These values can be used as defaults or referenced directly in your code.
# They are separated from secret keys for better modularity and security.

DEFAULT_LLM_PROVIDER: str = "openai/gpt-4o-mini"
DEFAULT_INSTRUCTION_TO_LLM: str = (
    "Navigate through this page to extract information about the specific service "
    "and map the service name to that information in JSON. Format results in JSON and "
    "include the name of the service, information about the service, and price. If there "
    "is no price, set it to null."
)
DEFAULT_MAX_TOKENS: int = 3000
DEFAULT_TEMPERATURE: float = 0.0
