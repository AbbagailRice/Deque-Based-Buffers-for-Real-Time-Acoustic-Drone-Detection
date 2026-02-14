"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:

Defines the AudioBuffer class which implements
a fixed-size rolling audio buffer using deque.

"""
#imports

from collections import deque
import numpy as np


class AudioBuffer:
    """
    A fixed-size rolling audio buffer.

    When the buffer reaches its maximum size,
    the oldest samples are automatically removed
    as new ones are added.
    """

    def __init__(self, max_samples: int):
        """
        Input: max_samples (int): Maximum number of samples to store.
        Output: None
        Details:
        Initialize the audio buffer.

        """
        # Store maximum capacity
        self.max_samples = max_samples

        # Create deque with fixed maximum length
        # Oldest samples are dropped automatically when full
        self._buffer = deque(maxlen=max_samples)

        # Store previous window for spike comparison
        # This will be used during analysis phase
        self._previous_window = None


    def add_samples(self, samples):
        """
        Input: samples (iterable): List, tuple, or NumPy array of samples.
        Output: None
        Details:
        Add multiple audio samples to the buffer.

        """
        # Extend appends elements in O(k) where k = len(samples)
        # If total size exceeds max_samples, oldest samples are discarded automatically
        self._buffer.extend(samples)


    def get_samples(self) -> np.ndarray:
        """
        Input: None
        Output: np.ndarray
        Details:
        Return current buffer contents as a NumPy array.
        """
        # Convert deque to NumPy array for FFT processing
        # Use float32 for realistic audio representation and lower memory overhead
        if len(self._buffer) == 0:
            return np.array([], dtype=np.float32)

        return np.array(self._buffer, dtype=np.float32)


    def get_window(self) -> np.ndarray:
        """
        Input: None
        Output: np.ndarray
        Details:
        Return current sliding window (alias for get_samples).
        """
        return self.get_samples()


    def store_previous_window(self):
        """
        Input: None
        Output: None
        Details:
        Store the current window for later comparison.
        """
        self._previous_window = self.get_samples()


    def get_previous_window(self):
        """
        Input: None
        Output: np.ndarray or None
        Details:
        Return previously stored window.
        """
        return self._previous_window


    def is_full(self) -> bool:
        """
        Input: None
        Output: bool
        Details:
        Return True if buffer has reached maximum capacity.
        """
        return len(self._buffer) == self.max_samples


    def clear(self):
        """
        Input: None
        Output: None
        Details:
        Remove all samples from the buffer.
        """
        self._buffer.clear()
        self._previous_window = None


    def __len__(self):
        """
        Input: None
        Output: int
        Details:    
            Return current number of stored samples.
            
        """
        return len(self._buffer)
