"""
Authors:    Abbagail Rice 
            Elizabeth Aristizabal
            Richard Baldwin

Date:   2026
Email:  agrice0@frostburg.edu
        laristizabal0@frostburg.edu
        rcbaldwin0@frostburg.edu

Description:

"""
#imports

import argparse
import configparser
from Detect import run_drone_detection

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
        "TARGET_FREQ": int(config.get("DETECTION", "TARGET_FREQ", fallback=265)),
        "THRESHOLD": int(config.get("DETECTION", "THRESHOLD", fallback=15)),
        "WINDOW_SIZE": int(config.get("DETECTION", "WINDOW_SIZE", fallback=10)),
        "MIN_MATCH_RATIO": float(config.get("DETECTION", "MIN_MATCH_RATIO", fallback=0.6))
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

    return parser.parse_args()
def main():
    """
    Input: None
    Output: None
    Details:
        Execute real-time drone detection loop using parameters
        loaded from configuration file, with optional command-line overrides.
    """

    args = parse_args()
    config = load_config(args.config)
    run_drone_detection(config)


if __name__ == "__main__":
    main()
