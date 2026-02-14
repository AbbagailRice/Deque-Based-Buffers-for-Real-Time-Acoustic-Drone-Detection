"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:

Defines FFT transformation and frequency-domain comparison
logic for real-time acoustic drone detection.

"""
#imports

import numpy as np


class DroneDetector:
    """
    Performs FFT transformation and spike detection
    between current and previous sliding windows.
    """

    def __init__(self, sample_rate: int, rpm_min: int = 4000, rpm_max: int = 12000):
        """
        Input: sample_rate (int), rpm_min (int), rpm_max (int)
        Output: None
        Details:
        Initialize detector parameters and RPM detection range.
        """
        # Audio sampling rate (e.g., 44100 Hz)
        self.sample_rate = sample_rate

        # RPM range of interest (drone propellers)
        self.rpm_min = rpm_min
        self.rpm_max = rpm_max

        # Convert RPM range to frequency (Hz)
        # RPM / 60 = revolutions per second
        self.freq_min = rpm_min / 60
        self.freq_max = rpm_max / 60


    def compute_fft(self, window: np.ndarray) -> np.ndarray:
        """
        Input: window (np.ndarray)
        Output: np.ndarray
        Details:
        Compute the real FFT (RFFT) of the time-domain window.
        """
        # Perform real FFT (O(n log n))
        fft_result = np.fft.rfft(window)

        # Return magnitude spectrum (absolute value)
        return np.abs(fft_result)


    def extract_frequency_band(self, spectrum: np.ndarray, window_size: int) -> np.ndarray:
        """
        Input: spectrum (np.ndarray), window_size (int)
        Output: np.ndarray
        Details:
        Extract the frequency band corresponding to drone RPM range.
        """
        # Generate frequency bins corresponding to RFFT output
        freqs = np.fft.rfftfreq(window_size, d=1/self.sample_rate)

        # Identify indices within drone frequency range
        indices = np.where((freqs >= self.freq_min) & (freqs <= self.freq_max))

        # Return only the relevant frequency magnitudes
        return spectrum[indices]


    def detect_spike(self, current_window: np.ndarray, previous_window: np.ndarray, threshold: float = 1000.0) -> bool:
        """
        Input: current_window (np.ndarray), previous_window (np.ndarray), threshold (float)
        Output: bool
        Details:
        Compare frequency-domain magnitude differences between
        current and previous windows to detect acoustic spikes.
        """
        # Compute FFT magnitudes for both windows
        current_fft = self.compute_fft(current_window)
        previous_fft = self.compute_fft(previous_window)

        # Extract drone-relevant frequency bands
        current_band = self.extract_frequency_band(current_fft, len(current_window))
        previous_band = self.extract_frequency_band(previous_fft, len(previous_window))

        # Compute difference between spectra (O(n))
        difference = np.abs(current_band - previous_band)

        # Determine if spike exceeds threshold
        return np.max(difference) > threshold
