from banking.exception import BankingException
from banking.logger import logging
from banking.config.configuration import Configuartion
from banking.component.data_ingestion import DataIngestion
import os
def main():
    try:
        print('Starting Demo app')
        config_path = os.path.join("config","config.yaml")
        config = Configuartion(config_file_path=config_path)
        data_ingestion = DataIngestion(data_ingestion_config=config.get_data_ingestion_config())
        data_ingestion.initiate_data_ingestion()        

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()