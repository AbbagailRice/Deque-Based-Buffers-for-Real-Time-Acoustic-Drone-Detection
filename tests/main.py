"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:

Main execution loop for real-time acoustic drone detection.
Loads configuration parameters from config.ini (or CLI override)
and simulates audio ingestion, sliding window buffering,
FFT transformation, and spike detection.

"""
#imports

import argparse
import numpy as np
import configparser
from audio_buffer import AudioBuffer, DroneDetector


def function():
    """
    Input: None
    Output: None
    Details:
        Placeholder for future expansion (e.g., real audio capture).
    """
    pass


def load_config(config_path: str = "config.ini") -> dict:
    """
    Input: config_path (str)
    Output: dict
    Details:
        Load configuration parameters from config.ini.
    """

    config = configparser.ConfigParser()
    config.read(config_path)

    return {
        "sample_rate": config.getint("AUDIO", "sample_rate"),
        "window_seconds": config.getint("AUDIO", "window_seconds"),
        "chunk_size": config.getint("AUDIO", "chunk_size"),
        "rpm_min": config.getint("DETECTION", "rpm_min"),
        "rpm_max": config.getint("DETECTION", "rpm_max"),
        "threshold": config.getfloat("DETECTION", "threshold"),
        "iterations": config.getint("SYSTEM", "iterations"),
    }


def parse_args() -> argparse.Namespace:
    """
    Input: None
    Output: argparse.Namespace
    Details:
        Parse command-line arguments for optional configuration overrides.
    """

    parser = argparse.ArgumentParser(
        description="Simulated real-time acoustic drone detection"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.ini",
        help="Path to configuration file (default: config.ini)"
    )

    parser.add_argument(
        "--iterations",
        type=int,
        help="Number of simulation iterations (overrides config.ini)"
    )

    parser.add_argument(
        "--chunk_size",
        type=int,
        help="Size of each audio chunk in samples (overrides config.ini)"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        help="Detection threshold (overrides config.ini)"
    )

    return parser.parse_args()


def run_simulation(audio_buffer: AudioBuffer, detector: DroneDetector,
                   chunk_size: int, iterations: int, threshold: float):
    """
    Input: 
        audio_buffer (AudioBuffer): Sliding window buffer
        detector (DroneDetector): FFT + spike detector
        chunk_size (int): Number of samples per simulated chunk
        iterations (int): Number of loop iterations
        threshold (float): Spike detection threshold
    Output: None
    Details:
        Simulates real-time audio ingestion and performs drone spike detection.
    """

    print("Starting simulated real-time drone detection loop...\n")

    for iteration in range(iterations):

        # Simulated audio chunk (replace with real capture later)
        new_samples = np.random.randn(chunk_size).astype(np.float32)

        # Add samples to sliding window buffer
        audio_buffer.add_samples(new_samples)

        # Only begin detection once full window is ready
        if audio_buffer.is_full():

            current_window = audio_buffer.get_window()
            previous_window = audio_buffer.get_previous_window()

            if previous_window is not None:

                detected = detector.detect_spike(
                    current_window,
                    previous_window,
                    threshold=threshold
                )

                if detected:
                    print(f"[Iteration {iteration}] Potential drone spike detected.")

            # Store current window for next comparison
            audio_buffer.store_previous_window()

    print("\nSimulation complete.")


def main():
    """
    Input: None
    Output: None
    Details:
        Execute real-time drone detection loop using parameters
        loaded from configuration file, with optional command-line overrides.
    """

    # Parse Command-Line Arguments

    args = parse_args()
    config = load_config(args.config)

    # Override config values if provided via CLI
    iterations = args.iterations if args.iterations is not None else config["iterations"]
    chunk_size = args.chunk_size if args.chunk_size is not None else config["chunk_size"]
    threshold = args.threshold if args.threshold is not None else config["threshold"]

    SAMPLE_RATE = config["sample_rate"]
    WINDOW_SECONDS = config["window_seconds"]
    BUFFER_SIZE = SAMPLE_RATE * WINDOW_SECONDS
    RPM_MIN = config["rpm_min"]
    RPM_MAX = config["rpm_max"]

    # Initialize Buffer and Detector

    audio_buffer = AudioBuffer(max_samples=BUFFER_SIZE)

    detector = DroneDetector(
        sample_rate=SAMPLE_RATE,
        rpm_min=RPM_MIN,
        rpm_max=RPM_MAX
    )

    print("Starting simulated real-time drone detection loop...\n")

    # Run Simulation

    run_simulation(
        audio_buffer=audio_buffer,
        detector=detector,
        chunk_size=chunk_size,
        iterations=iterations,
        threshold=threshold
    )


if __name__ == "__main__":
    main()
