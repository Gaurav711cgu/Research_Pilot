"""
Voice Interface — powered by Amazon Nova 2 Sonic.
Handles speech-to-text input and text-to-speech output.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import io
import os
import tempfile
from typing import Optional
from tools.bedrock_client import BedrockClient
from src.config import CONFIG


class VoiceInterface:
    """
    Amazon Nova 2 Sonic-powered voice interface for ResearchPilot.
    Provides:
    - Voice query capture (microphone → text)
    - Voice report delivery (text → speech)
    - Streaming audio support
    """

    def __init__(self):
        self.bedrock = BedrockClient()
        self.sample_rate = CONFIG.voice_sample_rate
        self.channels = CONFIG.voice_channels

    def listen(self, duration_seconds: int = 10) -> str:
        """
        Record audio from microphone and transcribe using Nova 2 Sonic.
        Returns the transcribed research query text.
        """
        try:
            import sounddevice as sd
            import numpy as np
            import soundfile as sf
        except ImportError:
            print("[VoiceInterface] Audio libraries not available, using text input")
            return self._text_fallback()

        print(f"[VoiceInterface] 🎤 Listening for {duration_seconds} seconds...")
        print("[VoiceInterface] Speak your research query now...")

        # Record audio
        recording = sd.rec(
            int(duration_seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"
        )
        sd.wait()
        print("[VoiceInterface] Recording complete. Transcribing...")

        # Convert to WAV bytes
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, recording, self.sample_rate, format="WAV")
        wav_bytes = wav_buffer.getvalue()

        # Transcribe with Nova 2 Sonic
        transcript = self.bedrock.speech_to_text(wav_bytes)
        print(f"[VoiceInterface] Transcribed: '{transcript}'")
        return transcript

    def speak(self, text: str, save_path: Optional[str] = None) -> bool:
        """
        Convert text to speech using Nova 2 Sonic and play it.
        Optionally saves to a file.
        Returns True if successful.
        """
        print("[VoiceInterface] 🔊 Converting to speech...")
        try:
            audio_bytes = self.bedrock.text_to_speech(text)

            if save_path:
                with open(save_path, "wb") as f:
                    f.write(audio_bytes)
                print(f"[VoiceInterface] Audio saved to {save_path}")

            # Play audio
            self._play_audio(audio_bytes)
            return True

        except Exception as e:
            print(f"[VoiceInterface] TTS error: {e}")
            print(f"[VoiceInterface] Text output: {text}")
            return False

    def _play_audio(self, audio_bytes: bytes) -> None:
        """Play audio bytes using sounddevice."""
        try:
            import sounddevice as sd
            import soundfile as sf

            wav_buffer = io.BytesIO(audio_bytes)
            data, samplerate = sf.read(wav_buffer)
            sd.play(data, samplerate)
            sd.wait()
        except ImportError:
            # Try platform-specific fallback
            self._system_play_fallback(audio_bytes)

    def _system_play_fallback(self, audio_bytes: bytes) -> None:
        """Save to temp file and play via system command."""
        import subprocess
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        try:
            if os.name == "posix":
                subprocess.run(["aplay", tmp_path], capture_output=True)
        except Exception:
            pass
        finally:
            os.unlink(tmp_path)

    def _text_fallback(self) -> str:
        """Text input fallback when audio is unavailable."""
        return input("Enter your research query: ")

    def speak_streamed(self, text: str) -> None:
        """
        Stream TTS output in chunks for low-latency voice delivery.
        Useful for long reports.
        """
        # Split into sentences for streaming
        sentences = text.replace("? ", "?|").replace(". ", ".|").replace("! ", "!|").split("|")
        for sentence in sentences:
            if sentence.strip():
                self.speak(sentence.strip())
