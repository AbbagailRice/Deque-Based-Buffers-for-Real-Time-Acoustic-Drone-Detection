# Detect.py
import numpy as np
import pyaudio
from collections import deque
import threading
import time


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = int(RATE * 0.5)  # 0.5 second chunks

def run_drone_detection(config, stop_event: threading.Event = None):
    """
    Run live drone detection. press enter to stop.
    """
    #vars
    #vars from config
    target_freq = config["TARGET_FREQ"]
    threshold = config["THRESHOLD"]
    window_size = config["WINDOW_SIZE"]
    min_match_ratio = config["MIN_MATCH_RATIO"]
    #other vars
    history = deque(maxlen=window_size)
    running = True
    """
    #old stop controller
    def monitor_input():
        nonlocal running
        while True:
            user_input = input().strip().lower()
            if user_input == 'end':
                running = False
                break

    # Start input listener thread
    threading.Thread(target=monitor_input, daemon=True).start()
    """
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print(f"Started drone detection (@{RATE}Hz)")
    #print("Type 'end' and press Enter to stop.")

    try:
        while running:
            if stop_event and stop_event.is_set():
                break
            
            start_time = time.perf_counter()

            # Read audio
            data_raw = stream.read(CHUNK, exception_on_overflow=False)
            data = np.frombuffer(data_raw, dtype=np.int16)

            # FFT
            windowed = data * np.hanning(len(data))
            fft = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(data), 1/RATE)

            # Magnitudes and noise blocking
            magnitudes = np.abs(fft)
            magnitudes[freqs < 150] = 0
            peak_index = np.argmax(magnitudes)
            peak_freq = freqs[peak_index]

            # History match check
            history.append(peak_freq)
            matches = sum(1 for f in history if abs(f - target_freq) <= threshold)
            match_ratio = matches / len(history)

            exec_time = time.perf_counter() - start_time

            # Detection feedback
            if len(history) == window_size and match_ratio >= min_match_ratio:
                print(f"!!! DRONE DETECTED !!! {peak_freq:.2f}Hz | Conf: {match_ratio*100:.0f}% | Time: {exec_time:.5f}s")
            else:
                print(f"Scanning... Peak: {peak_freq:.2f}Hz | Time: {exec_time:.5f}s", end='\r')

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        print("\nENDING")
        stream.stop_stream()
        stream.close()
        p.terminate()
