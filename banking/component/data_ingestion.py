from banking.entity.config_entity import DataIngestionConfig
import sys,os
from banking.exception import BankingException
from banking.logger import logging
from banking.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import wget
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise BankingException(e,sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:            
            self.download_and_extract_banking_data()            
            return self.split_data_as_train_test()
        
        except Exception as e:
            raise BankingException(e,sys) from e    

    def download_and_extract_banking_data(self,):
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url            

            #folder location to download file            
            extract_download_dir = self.data_ingestion_config.extract_download_dir            

            os.makedirs(extract_download_dir, exist_ok=True)
            banking_file_name = os.path.basename(download_url)
            extract_file_path = os.path.join(extract_download_dir, banking_file_name)
            
            # Download zip file to extract_download_dir
            logging.info(f"Downloading file from :[{download_url}] into :[{extract_file_path}]")                        
            wget.download(url=download_url, out=extract_download_dir)
            logging.info(f"File :[{extract_file_path}] has been downloaded successfully.")            

            # Create folder to extract from zip
            main_data_dir = self.data_ingestion_config.main_data_dir
            if os.path.exists(main_data_dir):
                os.remove(main_data_dir)

            os.makedirs(main_data_dir,exist_ok=True)

            # Extract downloaded zip
            logging.info(f"Extracting zip file: [{extract_file_path}] into dir: [{main_data_dir}]")            
            with ZipFile(extract_file_path,"r") as zip_ref:
                zip_ref.extractall(main_data_dir)
            logging.info(f"Extraction completed")            

        except Exception as e:
            raise BankingException(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            print('Inside split_data_as_train_test')
            main_data_dir = self.data_ingestion_config.main_data_dir
            file_name = os.listdir(main_data_dir)[2]
            banking_file_path = os.path.join(main_data_dir,file_name)


            logging.info(f"Reading input file: [{banking_file_path}]")
            banking_data_frame = pd.read_table(banking_file_path, sep = ' ')
            banking_data_frame.rename(columns = {'laufkont':'status', 'laufzeit':'duration', 'moral': 'credit_history', 
                                                 'verw': 'purpose', 'hoehe': 'amount', 'sparkont': 'savings', 
                                                 'beszeit': 'employment_duration', 'rate': 'installment_rate', 'famges': 'personal_status_sex', 
                                                 'buerge': 'other_debtors', 'wohnzeit': 'present_residence', 'verm': 'property', 
                                                 'alter': 'age', 'weitkred': 'other_installment_plans', 'wohn': 'housing', 
                                                 'bishkred': 'number_credits', 'beruf': 'job', 'pers': 'people_liable', 
                                                 'telef': 'telephone',  'gastarb':'foreign_worker', 'kredit': 'credit_risk'}, 
                                                 inplace = True)
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(banking_data_frame, banking_data_frame["credit_risk"]):
                strat_train_set = banking_data_frame.loc[train_index].drop(["credit_risk"],axis=1)
                strat_test_set = banking_data_frame.loc[test_index].drop(["credit_risk"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise BankingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
