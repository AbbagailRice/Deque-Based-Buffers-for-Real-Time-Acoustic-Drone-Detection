import numpy as np
import pyaudio
import time

# Constants
RATE = 48000
CHUNK = 24000  # 0.5 seconds
TARGET_FREQ = 245
THRESHOLD = 20
TEST_DURATION = 60

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, 
                input=True, frames_per_buffer=CHUNK)

print(f"Starting basic detection (@{RATE}Hz)...")
print("This version has no temporal filtering.")

# Tracking Var
alert_count = 0
total_cycles = 0
start_test_time = time.time()
end_trigger_time = start_test_time + TEST_DURATION

try:
    while time.time() < end_trigger_time:
        total_cycles += 1

        # Acquisition
        data_raw = stream.read(CHUNK, exception_on_overflow=False)
        data = np.frombuffer(data_raw, dtype=np.int16)

        # Processing (FFT)
        #start_math = time.perf_counter()
        windowed = data * np.hanning(len(data))
        fft = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(data), 1/RATE)
        
        magnitudes = np.abs(fft)
        magnitudes[freqs < 150] = 0  # High-pass filter
        peak_freq = freqs[np.argmax(magnitudes)]
        
        # Single-Frame Check
        is_match = abs(peak_freq - TARGET_FREQ) <= THRESHOLD
        
        #proc_time = (time.perf_counter() - start_math) * 1000
        remaining = end_trigger_time - time.time()
        

        if is_match:
            # ALERT
            alert_count += 1 
            print(f"ALERTS Peak: {peak_freq:.2f}Hz | Total Alerts: {alert_count}")
        else:
            print(f"Scanning... Peak: {peak_freq:.2f}Hz", end='\r')
            
    print("TEST COMPLETE (Timer Expired)")

except KeyboardInterrupt:
    print("\n" + "—"*30)
    print("TEST INTERRUPTED BY USER")

# Final Metrics
actual_end_time = time.time()
duration = actual_end_time - start_test_time

print(f"Total Duration:   {duration:.2f} seconds")
print(f"Total Cycles:     {total_cycles}")
print(f"Total False Positives: {alert_count}")

print("—"*30)

stream.stop_stream()
stream.close()
p.terminate()