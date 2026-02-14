"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:
Test AudioBuffer functionality
"""

import numpy as np
import pytest
from audio_buffer import AudioBuffer

def test_add_and_get_samples():
    """
    Input: None
    Output: None
    Details:
        Test that samples can be added to the buffer
        and retrieved correctly.
    """
    buf = AudioBuffer(max_samples=10)
    samples = np.arange(5)
    buf.add_samples(samples)

    retrieved = buf.get_samples()
    assert np.array_equal(retrieved, samples), "Buffer did not return expected samples"

def test_buffer_overflow():
    """
    Input: None
    Output: None
    Details:
        Test that buffer discards oldest samples when over capacity.
    """
    buf = AudioBuffer(max_samples=5)
    buf.add_samples(np.arange(7))  # add more than max
    retrieved = buf.get_samples()

    # Should only contain last 5 elements
    assert np.array_equal(retrieved, np.array([2,3,4,5,6])), "Overflow handling failed"

def test_clear_and_length():
    """
    Input: None
    Output: None
    Details:
        Test clearing buffer and __len__ method.
    """
    buf = AudioBuffer(max_samples=5)
    buf.add_samples([1,2,3])
    assert len(buf) == 3, "__len__ returned incorrect value"

    buf.clear()
    assert len(buf) == 0, "Buffer was not cleared properly"
