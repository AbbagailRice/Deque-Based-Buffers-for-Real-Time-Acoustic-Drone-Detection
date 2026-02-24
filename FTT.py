import numpy as np
from scipy.io import wavfile
from collections import deque

# Load recording
samplerate, data = wavfile.read('HS1.wav')

# If stereo, take only one channel
if len(data.shape) > 1:
    data = data[:, 0]

def get_dominant_freq(chunk, rate):
    # Apply FFT
    windowed_chunk = chunk * np.hanning(len(chunk)) # Smooth the edges
    fft_data = np.fft.rfft(windowed_chunk)
    freqs = np.fft.rfftfreq(len(chunk), 1/rate)
    
    # Find the peak (magnitude)
    magnitude = np.abs(fft_data)
    peak_index = np.argmax(magnitude)
    return freqs[peak_index]

# Set up deque
# Let's say we check every 0.5 seconds of audio
chunk_size = int(samplerate * .5)
history = deque(maxlen=10) # 5 seconds of history

for i in range(0, len(data), chunk_size):
    chunk = data[i : i + chunk_size]
    if len(chunk) < chunk_size: break
    
    peak = get_dominant_freq(chunk, samplerate)
    history.append(peak)
    
    print(f"Current Window Peak: {peak:.2f} Hz")