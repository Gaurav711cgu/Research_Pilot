"""
ResearchPilot Configuration
Amazon Nova AI Hackathon 2026
"""
import os
from dataclasses import dataclass

@dataclass
class NovaConfig:
    # AWS Bedrock settings
    aws_region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # Amazon Nova model IDs
    nova_pro_model_id: str = "amazon.nova-pro-v1:0"
    nova_lite_model_id: str = "amazon.nova-lite-v1:0"
    nova_sonic_model_id: str = "amazon.nova-sonic-v1:0"
    nova_embed_model_id: str = "amazon.nova-embed-v1:0"

    # Nova Act
    nova_act_api_key: str = os.getenv("NOVA_ACT_API_KEY", "")

    # Research settings
    max_web_sources: int = 10
    max_doc_pages: int = 50
    search_depth: int = 3          # How many pages deep to browse
    parallel_agents: int = 3       # Number of parallel research agents
    confidence_threshold: float = 0.75  # Below this → human escalation
    max_report_length: int = 5000  # characters
    extended_thinking_budget: int = 8000  # tokens for Nova Pro reasoning

    # Voice settings
    voice_sample_rate: int = 16000
    voice_channels: int = 1
    tts_voice: str = "matthew"     # Nova Sonic voice

CONFIG = NovaConfig()
