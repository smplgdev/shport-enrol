import logging
import os
import sys


def setup_logging():
    debug = os.getenv("DEBUG") in ["True", "true", "1"]
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
