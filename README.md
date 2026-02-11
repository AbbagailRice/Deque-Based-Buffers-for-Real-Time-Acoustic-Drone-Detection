# Deque-Based-Buffers-for-Real-Time-Acoustic-Drone-Detection
Theoretical vs. Experimental Efficiency of Deque-Based Buffers for Real-Time Acoustic Drone Detection
# Theoretical vs. Experimental Efficiency of Deque-Based Buffers for Real-Time Acoustic Drone Detection

**Team GOAT**
* **Abbagail Rice** (Primary POC & Lead Documentation)
* **Liz Aristizabal**
* **Richard Baldwin**
* **Advisor:** Dr. Nooh A Bany Muhammad

**Frostburg State University | Spark Labs | CCIT**

---

## Project Overview
This project explores a deterministic, lightweight approach to real-time acoustic drone detection. By utilizing **Deque structures** and **Fast Fourier Transforms (FFT)**, we aim to identify unique harmonic signatures of drones ($4,000$ to $12,000$ RPM) with minimal latency on standard consumer hardware.

## Technical Workflow
- **Capture:** Continuous live audio ingestion via Blue Yeti or System Loopback.
- **Buffer:** A 5-second `collections.deque` serves as a high-speed sliding window.
- **Transform:** Time Domain waves are converted to Frequency Domain pitch via RFFT.
- **Analysis:** "Current" window is checked against the "Previous" card in the deque to detect sudden acoustic spikes.

---

## Project Timeline (Spring 2026)
| Phase | Goal | Target Completion |
| :--- | :--- | :--- |
| **I. Baseline** | Record drone "Fingerprints" and calibrate Yeti/Loopback levels. | Feb 18 |
| **II. Implementation** | Finalize "Ongoing" loop code & Deque-to-FFT logic. | Mar 2 |
| **III. Theoretical** | Line-by-line Primitive Operation analysis & Big-O calculation. | Mar 11 |
| **IV. Experimental** | Collect execution time data and CPU latency metrics. | Mar 21 |
| **V. Drafting** | Writing Methodology, Motivation, and Solution sections. | Mar 30 |
| **VI. Final Draft** | **Complete Draft Finished** | **April 5** |

---

## Theoretical Analysis (In-Progress)
| Statement | Primitive Operations | Complexity |
| :--- | :--- | :--- |
| `deque.append()` | 1 method call, 1 assignment | $O(1)$ |
| `np.fft.rfft(window)` | Butterfly algorithm ops | $O(n \log n)$ |
| `current - previous` | $n/2$ subtractions | $O(n)$ |

---

## Prerequisites
- Python 3.10+
- PyAudio / PyAudioWPatch
- NumPy
