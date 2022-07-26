from sklearn.pipeline import Pipeline
from banking.exception import BankingException
from banking.logger import logging
from banking.config.configuration import Configuartion
from banking.component.data_ingestion import DataIngestion
from banking.pipeline.pipeline import Pipeline
from banking.config.configuration import Configuartion

import os

def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        pipeline.start()
        logging.info("main function execution completed.")

        #pipeline = Pipeline()
        #pipeline.run_pipeline()

        #config_path = os.path.join("config","config.yaml")
        #config = Configuartion(config_file_path=config_path)
        
        #data_ingestion = DataIngestion(data_ingestion_config=config.get_data_ingestion_config())
        #data_ingestion.initiate_data_ingestion()                

        #data_validation_config = Configuartion().get_data_validation_config()
        #print(data_validation_config)

        #data_transformation_config = Configuartion().get_data_transformation_config()
        #print(data_transformation_config)

        #model_trainer_config = Configuartion().get_model_trainer_config()
        #print(model_trainer_config)

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()