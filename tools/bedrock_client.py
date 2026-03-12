"""
Centralized Amazon Bedrock client for all Nova model calls.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import json
import boto3
import base64
from typing import Any, Optional
from src.config import CONFIG


class BedrockClient:
    """
    Unified client for all Amazon Nova model invocations via Amazon Bedrock.
    Supports: Nova Pro, Nova Lite, Nova Sonic, Nova Embeddings.
    """

    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=CONFIG.aws_region,
            aws_access_key_id=CONFIG.aws_access_key,
            aws_secret_access_key=CONFIG.aws_secret_key,
        )

    # ─────────────────────────────────────────
    # NOVA 2 PRO — Text + Multimodal Reasoning
    # ─────────────────────────────────────────
    def invoke_nova_pro(
        self,
        prompt: str,
        system_prompt: str = "",
        image_base64: Optional[str] = None,
        image_mime: str = "image/png",
        extended_thinking: bool = False,
        max_tokens: int = 4096,
    ) -> str:
        """
        Invoke Amazon Nova 2 Pro for reasoning, analysis, synthesis.
        Supports text + image inputs. Optional extended thinking mode.
        """
        content = []

        # Add image if provided (multimodal)
        if image_base64:
            content.append({
                "image": {
                    "format": image_mime.split("/")[-1],
                    "source": {
                        "bytes": base64.b64decode(image_base64)
                    }
                }
            })

        content.append({"text": prompt})

        body = {
            "messages": [{"role": "user", "content": content}],
            "inferenceConfig": {
                "maxNewTokens": max_tokens,
                "temperature": 0.3,
            }
        }

        if system_prompt:
            body["system"] = [{"text": system_prompt}]

        # Extended thinking for deep reasoning tasks
        if extended_thinking:
            body["additionalModelRequestFields"] = {
                "thinking": {
                    "type": "enabled",
                    "budget_tokens": CONFIG.extended_thinking_budget
                }
            }

        response = self.client.invoke_model(
            modelId=CONFIG.nova_pro_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        return result["output"]["message"]["content"][0]["text"]

    # ─────────────────────────────────────────
    # NOVA 2 LITE — Fast Structured Output
    # ─────────────────────────────────────────
    def invoke_nova_lite(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 2048,
    ) -> str:
        """
        Invoke Amazon Nova 2 Lite for fast, cost-efficient text generation.
        Ideal for structured JSON output, summaries, formatting tasks.
        """
        body = {
            "messages": [
                {"role": "user", "content": [{"text": prompt}]}
            ],
            "inferenceConfig": {
                "maxNewTokens": max_tokens,
                "temperature": 0.1,  # Low temp for structured output
            }
        }

        if system_prompt:
            body["system"] = [{"text": system_prompt}]

        response = self.client.invoke_model(
            modelId=CONFIG.nova_lite_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        return result["output"]["message"]["content"][0]["text"]

    # ─────────────────────────────────────────
    # NOVA MULTIMODAL EMBEDDINGS
    # ─────────────────────────────────────────
    def embed_text(self, text: str) -> list[float]:
        """
        Generate semantic embeddings for text using Nova Multimodal Embeddings.
        Used for semantic similarity ranking of research sources.
        """
        body = {
            "inputText": text[:2048]  # Truncate to model limit
        }

        response = self.client.invoke_model(
            modelId=CONFIG.nova_embed_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        return result["embedding"]

    def embed_image(self, image_base64: str) -> list[float]:
        """
        Generate multimodal embeddings for an image.
        Used for visual content similarity search.
        """
        body = {
            "inputImage": image_base64
        }

        response = self.client.invoke_model(
            modelId=CONFIG.nova_embed_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        return result["embedding"]

    # ─────────────────────────────────────────
    # NOVA 2 SONIC — Speech I/O (via Bedrock)
    # ─────────────────────────────────────────
    def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech using Amazon Nova 2 Sonic.
        Returns raw audio bytes (PCM/WAV).
        """
        body = {
            "text": text,
            "voiceConfig": {
                "voiceId": CONFIG.tts_voice
            }
        }

        response = self.client.invoke_model(
            modelId=CONFIG.nova_sonic_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="audio/wav",
        )

        return response["body"].read()

    def speech_to_text(self, audio_bytes: bytes) -> str:
        """
        Transcribe speech audio to text using Amazon Nova 2 Sonic.
        Returns transcribed text string.
        """
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        body = {
            "audio": {
                "format": "wav",
                "source": {"bytes": audio_b64}
            }
        }

        response = self.client.invoke_model(
            modelId=CONFIG.nova_sonic_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        return result.get("transcript", "")
