# Detect.py
import numpy as np
import pyaudio
from collections import deque
from threading import Event
import time



def run_drone_detection(config, stop_event: Event = None):
    """
    Run live drone detection. press enter to stop.
    """
    #vars
    #vars from config
    target_freq = config["TARGET_FREQ"]
    threshold = config["THRESHOLD"]
    window_size = config["WINDOW_SIZE"]
    min_match_ratio = config["MIN_MATCH_RATIO"]

    format_pyaudio = getattr(pyaudio, config.get("FORMAT", "paInt16"))
    channels = config.get("CHANNELS", 1)
    rate = config.get("RATE", 48000)
    chunk = int(rate * float(config.get("CHUNK_SEC", 0.5)))
    min_freq = config.get("MIN_FREQ", 150)

    freq_decimals = int(config.get("PRINT_FREQ_DECIMALS", 2))
    conf_decimals = int(config.get("PRINT_CONF_DECIMALS", 0))
    time_decimals = int(config.get("PRINT_TIME_DECIMALS", 5))
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
    stream = p.open(format=format_pyaudio, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk)

    print(f"Started drone detection (@{rate}Hz)")
    #print("Type 'end' and press Enter to stop.")

    try:
        while running:
            if stop_event and stop_event.is_set():
                break
            
            start_time = time.perf_counter()

            # Read audio
            data_raw = stream.read(chunk, exception_on_overflow=False)
            data = np.frombuffer(data_raw, dtype=np.int16)

            # FFT
            windowed = data * np.hanning(len(data))
            fft = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(data), 1/rate)

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
                print(f"!!! DRONE DETECTED !!! {peak_freq:.{freq_decimals}f}Hz | Conf: {match_ratio*100:.{conf_decimals}f}% | Time: {exec_time:.{time_decimals}f}s")
            else:
                print(f"Scanning... Peak: {peak_freq:.2f}Hz | Time: {exec_time:.5f}s", end='\r')

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        print("\nENDING")
        stream.stop_stream()
        stream.close()
        p.terminate()
