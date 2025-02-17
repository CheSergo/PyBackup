import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)
today = datetime.today()
log_name = today.strftime("%Y-%m-%d")
path = Path(f"./logs/{log_name}")
try:
    os.makedirs(path.parent, exist_ok=True)
except OSError as e:
    logger.error(f"Failed to create directories and file: {str(e)}")

logging.basicConfig(
    filename=path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
