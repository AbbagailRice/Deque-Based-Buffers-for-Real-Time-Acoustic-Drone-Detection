"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:
Test DroneDetector functionality
"""

import numpy as np
import pytest
from audio_buffer import DroneDetector

def test_compute_fft_placeholder():
    """
    Input: None
    Output: None
    Details:
        Placeholder test for FFT computation.
    """
    detector = DroneDetector(sample_rate=44100)
    window = np.random.randn(1024)
    fft_result = detector.compute_fft(window)

    assert fft_result.shape[0] == 513, "FFT output shape mismatch for RFFT"

def test_extract_frequency_band_placeholder():
    """
    Input: None
    Output: None
    Details:
        Placeholder test for frequency band extraction.
    """
    detector = DroneDetector(sample_rate=44100)
    window = np.random.randn(1024)
    spectrum = detector.compute_fft(window)
    band = detector.extract_frequency_band(spectrum, window_size=1024)

    # Just check that returned array is not empty
    assert band.size > 0, "Frequency band extraction failed"

def test_detect_spike_placeholder():
    """
    Input: None
    Output: None
    Details:
        Placeholder test for spike detection logic.
    """
    detector = DroneDetector(sample_rate=44100)
    window = np.random.randn(1024).astype(np.float32)
    previous_window = np.copy(window)

    # Artificially inject a spike in current window
    window[100] += 10000

    detected = detector.detect_spike(window, previous_window, threshold=5000)
    assert detected, "Spike detection failed on artificial spike"
