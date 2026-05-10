
from pathlib import Path
from yaml import safe_load


#Layer2: Hardened System Prompt (from YAML)
def load_system_prompt(agent_name: str) -> str:
    """Load the system prompt for the agent from a YAML file."""
    prompt_file = Path("prompts") / "support_agent_v1.yaml"
    if not prompt_file.exists():
        raise ValueError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        data = safe_load(f)
    
    return data.get(agent_name)