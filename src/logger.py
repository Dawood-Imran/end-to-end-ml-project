# We log different information in some text file. The data can be exceptin which occurs in the code or every detail to track

import logging
import os
from datetime import datetime


# Creating a log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    
    ) 

logger = logging.getLogger(__name__)

if __name__=="__main__":
    logging.info("Logging has started")