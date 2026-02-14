"""
audio_buffer package

Exposes core components for real-time acoustic drone detection.

Modules:
- AudioBuffer: Sliding window deque-based buffer
- DroneDetector: FFT transformation and spike detection logic
"""

from .buffer import AudioBuffer
from .detector import DroneDetector

# Defines what gets imported when using:
# from audio_buffer import *
__all__ = ["AudioBuffer", "DroneDetector"]
