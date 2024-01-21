import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# All messages (including info) are routed to stderr.
# This enables for streaming data to stdout and piping the output of this script to another script
handler = logging.StreamHandler(sys.stderr)

handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
