import os
import logging
import datetime

LOG_FILE =f" {datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log"
log_path = os.path.join(os.getcwd() , "logs" , LOG_FILE)
os.makedirs(log_path , exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path , LOG_FILE)
logging.basicConfig(
    filename = LOG_FILE_PATH,
     format= "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

if __name__ == '__main__':
    logging.info("Logging Started..")