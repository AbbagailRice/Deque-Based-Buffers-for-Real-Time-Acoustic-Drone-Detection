import numpy as np
import pyaudio
from collections import deque
from threading import Event
import time

def run_drone_detection(config, stop_event: Event = None):
    # Vars from config
    target_freq = config["TARGET_FREQ"]
    threshold = config["THRESHOLD"]
    window_size = config["WINDOW_SIZE"]
    min_match_ratio = config["MIN_MATCH_RATIO"]

    # TEST VARS
    alert_count = 0
    total_cycles = 0
    start_test_time = time.time()
    test_duration = 60  # 60 seconds
    end_trigger_time = start_test_time + test_duration
    # --------------------------

    format_pyaudio = getattr(pyaudio, config.get("FORMAT", "paInt16"))
    channels = config.get("CHANNELS", 1)
    rate = config.get("RATE", 48000)
    chunk = int(rate * float(config.get("CHUNK_SEC", 0.5)))
    
    history = deque(maxlen=window_size)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=format_pyaudio, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk)

    print(f"Started 60s Drone Detection Test (@{rate}Hz)")
    print(f"Plan: Hum for 3s every 5s. Auto-stop in {test_duration}s.")

    try:
        # Loop runs only until the 60s timer expires
        while time.time() < end_trigger_time:
            if stop_event and stop_event.is_set():
                break

            total_cycles += 1
            start_total = time.perf_counter()
            
            # Read audio
            data_raw = stream.read(chunk, exception_on_overflow=False)
            data = np.frombuffer(data_raw, dtype=np.int16)

            # FFT & Processing
            windowed = data * np.hanning(len(data))
            fft = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(data), 1/rate)

            magnitudes = np.abs(fft)
            magnitudes[freqs < 150] = 0
            peak_freq = freqs[np.argmax(magnitudes)]

            # Deque Logic
            history.append(peak_freq)
            matches = sum(1 for f in history if abs(f - target_freq) <= threshold)
            match_ratio = matches / len(history)

            exec_time = time.perf_counter() - start_total 
            remaining = end_trigger_time - time.time()

            # Detection feedback
            if len(history) == window_size and match_ratio >= min_match_ratio:
                alert_count += 1
                print(f"!!! DRONE DETECTED !!! {peak_freq:.2f}Hz | Conf: {match_ratio*100:.0f}% | Left: {remaining:.1f}s")
            else:
                print(f"Scanning... Cycles: {total_cycles} | Alerts: {alert_count} | Left: {remaining:.1f}s", end='\r')

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        # Test summary
        actual_duration = time.time() - start_test_time
        print("\n" + "—"*30)
        print("60-SECOND TEST COMPLETE")
        print(f"Total Duration:   {actual_duration:.2f} seconds")
        print(f"Total Cycles:     {total_cycles}")
        print(f"Total Alerts:     {alert_count}")
        
        print("—"*30)
        
        stream.stop_stream()
        stream.close()
        p.terminate()