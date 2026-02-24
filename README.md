# Deque-Based-Buffers-for-Real-Time-Acoustic-Drone-Detection
Theoretical vs. Experimental Efficiency of Deque-Based Buffers for Real-Time Acoustic Drone Detection
# Theoretical vs. Experimental Efficiency of Deque-Based Buffers for Real-Time Acoustic Drone Detection

**Team**
* **Abbagail Rice** (Primary POC & Lead Documentation)
* **Liz Aristizabal**
* **Richard Baldwin**
* **Advisor:** Dr. Nooh A Bany Muhammad

**Frostburg State University | Spark Labs | CCIT**

---

## Project Overview
This project explores a deterministic, lightweight approach to real-time acoustic drone detection. By utilizing **Deque structures** and **Fast Fourier Transforms (FFT)**, we aim to identify unique harmonic signatures of drones.

## Technical Workflow
- **Capture:** Continuous live audio ingestion via Blue Yeti or System Loopback.
- **Buffer:** A 5-second `collections.deque` serves as a high-speed sliding window.
- **Transform:** Time Domain waves are converted to Frequency Domain pitch via RFFT.
- **Analysis:** "Current" window is checked against the "Previous" card in the deque to detect sudden acoustic spikes.


## Inside Detect.py, you can tweak these three lines to try to improve res:

TARGET_FREQ = 265: Set this to Hz of the drone motors you are detecting.

THRESHOLD = 15: How many Hz away from the target you allow.

MIN_MATCH_RATIO = 0.6: Higher means fewer false positives; lower means it’s easier to catch the drone.

## Prerequisites
- Python 3.10+
- PyAudio / PyAudioWPatch
- NumPy
