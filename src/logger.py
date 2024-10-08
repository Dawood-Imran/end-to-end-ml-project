import logging
import os
from datetime import datetime

# Creating a log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the path to the logs directory relative to the 'src' directory
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')  # 'logs' folder in the same directory as 'src'

# Create the logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Now, define the full path to the log file by combining the directory and file name
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Configure the logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Logging has started")
