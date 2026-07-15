
import os 
from from_root import from_root
import logging 
from datetime import datetime

log_file = f"{datetime.now().strftime('%B %d, %Y %H-%M-%S')}.log"
log_folder = os.path.join(from_root(),"LOGGER")
os.makedirs(log_folder,exist_ok=True)
log_filepath = os.path.join(log_folder,log_file)
format_logging='[%(asctime)s - %(name)s - %(levelname)s - %(filename)s ] %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=format_logging,
    datefmt="%B %d, %Y %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)




