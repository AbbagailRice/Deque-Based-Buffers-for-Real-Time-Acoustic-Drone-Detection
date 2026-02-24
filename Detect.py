import numpy as np
import pyaudio
from collections import deque
import threading
import time

# param based on init drone test
TARGET_FREQ = 265    
THRESHOLD = 15  # might need to be inc     
WINDOW_SIZE = 10     
MIN_MATCH_RATIO = 0.6 

# audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = int(RATE * 0.5) # 0.1 second chunks might change to .5s

history = deque(maxlen=WINDOW_SIZE)
running = True

# will end audio capture
def monitor_input():
    global running
    while True:
        user_input = input().strip().lower()
        if user_input == 'end':
            running = False
            break

# start the listener thread for ending
threading.Thread(target=monitor_input, daemon=True).start()

# init pyaudio interface
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

print(f"Started drone detection (@{RATE}Hz)")
print("Type 'end' and press Enter to stop.")

try:
    while running:
        start_time = time.perf_counter() # for experimental study section our timer to check time of each loop
        
        # start live audio capture
        data_raw = stream.read(CHUNK, exception_on_overflow=False)
        data = np.frombuffer(data_raw, dtype=np.int16)
        
        # FFT
        windowed = data * np.hanning(len(data))
        fft = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(data), 1/RATE)
        
        #can let us block room noise
        magnitudes = np.abs(fft)
        magnitudes[freqs < 150] = 0
        peak_index = np.argmax(magnitudes)
        peak_freq = freqs[peak_index]


        # deque history macht check
        history.append(peak_freq)
        matches = sum(1 for f in history if abs(f - TARGET_FREQ) <= THRESHOLD)
        match_ratio = matches / len(history)
        
        # end timer for experimental study section
        end_time = time.perf_counter()
        exec_time = end_time - start_time
        
        # feedback for detection
        if len(history) == WINDOW_SIZE and match_ratio >= MIN_MATCH_RATIO:
            print(f"!!! DRONE DETECTED !!! {peak_freq:.2f}Hz | Conf: {match_ratio*100:.0f}% | Time: {exec_time:.5f}s")
        else:
            print(f"Scanning... Peak: {peak_freq:.2f}Hz | Time: {exec_time:.5f}s", end='\r')

# deal wth any weird errors
except Exception as e:
    print(f"\nError: {e}")

# cleanup
finally:
    print("\nENDING")
    stream.stop_stream()
    stream.close()
    p.terminate()